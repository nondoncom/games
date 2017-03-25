
from tkinter import *
from tkinter.ttk import *
from solver import isSolvable, solve, genRandomBoard, calcTotalCost
from puzzle import NPuzzle
from threading import Thread
from time import sleep, time

class Tile():
  def __init__(self, canvas, value, pos, dim):
    self.canvas = canvas
    self.value = value
    self.pos = pos
    self.dim = dim
    self.rectangle = None
    self.label = None
    self.draw(self.canvas)
  
  def draw(self, canvas):
    self.rectangle = canvas.create_rectangle(*self.pos,*list(map(lambda a, b: a+b, self.pos, self.dim)))
    center = list(map(lambda a, b: a+(b/2), self.pos, self.dim))
    self.label = canvas.create_text(*center, text=str(self.value))

  def move(self, pos):
    self.canvas.move(self.label, *list(map(lambda a,b: b-a, map(lambda a, b: a+(b/2), self.pos, self.dim), map(lambda a, b: a+(b/2), pos, self.dim))))
    self.canvas.move(self.rectangle, *list(map(lambda a,b: b-a, self.pos, pos)))
    self.pos = pos

class ZeroTile(Tile):
  def __init__(self, canvas, pos, dim):
    Tile.__init__(self, canvas, 0, pos, dim)
  
  def draw(self, canvas):
    pass
    
  def move(self, pos):
    self.pos = pos

def buildTile(canvas, value, pos, dim):
  if value == 0:
    return ZeroTile(canvas, pos, dim)
  else:
    return Tile(canvas, value, pos, dim)

def swap(pos):
  return (pos[1],pos[0])

class Move():
  def __init__(self, tile, newPos, delay=0, v=0.1):
    self.tile = tile
    self.startPos = tile.pos
    self.newPos = newPos
    self.delay = delay
    self.v = v
    self.cv = v
    

class UI():
  choices = ['3', '4', '5', '6']
  moves = { "DOWN":(-1,0), "UP":(1,0), "LEFT":(0,1), "RIGHT":(0,-1) }
  
  def __init__(self):
    self.game = None
    self.tiles = []
    self.animations = []
    self.animationFrames = 30
    self.animationRate = 1000 // self.animationFrames
    self.__createWindow()
    self.__connectEvents()
    self._sizeChanged(self.getSize())

  def start(self):
    self.root.mainloop()

  def getSize(self):
    return int(self.boardSize.get())
    
  def __createWindow(self):
    self.root = Tk()
    self.root.title("N Puzzle")
    self.__createOptions()
    self.__createCanvas()
    self.__createActions()
    
  def __createOptions(self):
    optionFrame = Frame(self.root)
    optionFrame.grid(row=0, column=0, sticky=(N,W,E,S))
    optionFrame.columnconfigure(0, weight = 1)
    optionFrame.rowconfigure(0, weight = 1)
    optionFrame.pack(padx=10,pady=10)
    self.boardSize = StringVar(self.root)
    Label(optionFrame, text="N: ").grid(row=1,column=1)
    popupMenu = OptionMenu(optionFrame, self.boardSize, UI.choices[1], *UI.choices)
    popupMenu.grid(row=1,column=2)

  def __createCanvas(self):
    canvasFrame = Frame(self.root)
    canvasFrame.pack(padx=10,pady=10)
    self.canvas = Canvas(canvasFrame)
    self.canvas.grid(row=2, column=1, columnspan=2, sticky=(N,W,E,S))
    self.canvas.pack()
    self.canvas.config(background='yellow')
  
  def __createActions(self):
    actionFrame = Frame(self.root)
    actionFrame.pack(padx=10,pady=10)
    
    randomizeButton = Button(actionFrame, text="Randomize", command=lambda:self._actionSelected("RANDOMIZE") )
    randomizeButton.grid(row=3,column=1, sticky=(N,W,E,S))
    
    solveButton = Button(actionFrame, text="Solve", command=lambda:self._actionSelected("SOLVE") )
    solveButton.grid(row=3,column=2, sticky=(N,W,E,S))

  def __connectEvents(self):
    def dropdownSelected(*args):
      self._sizeChanged(self.boardSize.get())
    self.boardSize.trace('w', dropdownSelected)
    
    def canvasClick(event):
      pos = swap(UI.getTileFromPosition(event.x, event.y, self.canvas.winfo_width(), self.canvas.winfo_height(), self.game.size))
      self._moveTileTo(pos)
    self.canvas.bind("<Button-1>", canvasClick)

    def keyPressed(event):
      move = None
      if event.keycode == 40:
        move = "DOWN"
      elif event.keycode == 38:
        move = "UP"
      elif event.keycode == 37:
        move = "LEFT"
      elif event.keycode == 39:
        move = "RIGHT"
      self._processMove(move)
    self.root.bind('<Left>', keyPressed)
    self.root.bind('<Right>', keyPressed)
    self.root.bind('<Up>', keyPressed)
    self.root.bind('<Down>', keyPressed)
    
    self.root.after(500, lambda : self._buildTiles())
    self.root.after(self.animationRate, self._animate)

  def _buildTiles(self):
    self.canvas.delete(ALL)
    self.tiles = []
    w = int(self.canvas.winfo_width() / self.game.size)
    h = int(self.canvas.winfo_height() / self.game.size)
    for i in range(self.game.size):
      self.tiles.append([])
      for j in range(self.game.size):
        x = i*w
        y = j*h
        self.tiles[i].append(buildTile(self.canvas, self.game.board[j][i], (x, y), (w, h)))

  def getTileFromPosition(x, y, w, h, n):
    bw = w/n
    bh = h/n
    return (int(x/bw), int(y/bh))
        
  def calcPosition(pos, dim):
    return tuple(map(lambda a,b: a*b, pos, dim))

  def _moveTileFromTo(self, fromPos, toPos, delay=0):
    if self.tiles:
      fromRC = swap(fromPos)
      toRC = swap(toPos)
      self.tiles[toRC[0]][toRC[1]].move(UI.calcPosition(fromRC, self.tiles[toRC[0]][toRC[1]].dim))
      self.animations.append(Move(self.tiles[fromRC[0]][fromRC[1]], UI.calcPosition(toRC,self.tiles[fromRC[0]][fromRC[1]].dim), delay=delay))
      self.tiles[fromRC[0]][fromRC[1]], self.tiles[toRC[0]][toRC[1]] = self.tiles[toRC[0]][toRC[1]], self.tiles[fromRC[0]][fromRC[1]]
  
  def _moveTileTo(self, pos, delay=0):
    zero = self.game.zero
    if self.game.move(pos):
      self._moveTileFromTo(pos, zero, delay)
    else:
      print("Bad Move:", pos)
  
  def makeMoves(self, listOfMoves, delay=200):
    d = delay
    for i, x in enumerate(listOfMoves):
      self._processMove(x, d)
      d += delay
  
  def _sizeChanged(self, value):
    n = int(value)
    board = genRandomBoard(n)
    while not isSolvable(board):
      board = genRandomBoard(n)
    self.game =  NPuzzle(board)
    self._buildTiles()
  
  def _actionSelected(self, value):
    if value == "SOLVE":
      def endCallback(game):
        self.makeMoves(game.moves)
      pop = PopUp()
      pop.solve(self.game.board, endCallback)
      pop.mainloop()
    elif value == "RANDOMIZE":
      self._sizeChanged(self.getSize())
  
  def _processMove(self, move, delay=0):
    if move in UI.moves:
      pos = tuple(map(lambda a, b: a+b, self.game.zero, UI.moves[move]))
      if min(*pos) < 0 or max(*pos) >= self.game.size:
        print("Bad Move:", move)
      else:
        self._moveTileTo(pos, delay)
  
  def _animate(self):
    i = 0
    v = 0.1
    while i < len(self.animations):
      x = self.animations[i]
      if x.delay > 0:
        x.delay -= self.animationRate
        if x.delay <= 0:
          x.startPos = x.tile.pos
        i+=1
        continue
      x.cv += v
      if x.cv >= 1:
        x.tile.move(x.newPos)
        del self.animations[i]
      else:
        newPos = tuple(map(lambda a, b: int(a+((b-a)*x.cv)), x.startPos, x.newPos))
        x.tile.move(newPos)
        i+=1
    self.canvas.update()
    self.root.after(self.animationRate, self._animate)

class PopUp(Tk):
  def __init__(self, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    self.title("N Puzzle Solver")
    self.canceled = False
    self.__createContent()
    self.numberOf = 0
    self.startTime = time()
    
  def __createContent(self):
    mainFrame = Frame(self)
    mainFrame.grid(row=0, column=0, sticky=(N,W,E,S))
    mainFrame.columnconfigure(0, weight = 1)
    mainFrame.rowconfigure(0, weight = 1)    
    mainFrame.pack(padx=10,pady=10)
    
    self.progressbar = Progressbar(mainFrame, orient="horizontal", length=200, mode="determinate")
    self.progressbar.grid(row=1,column=1, columnspan=3, sticky=(N,W,E,S))


    self.timeVariable = StringVar(self)
    self.depthVariable = StringVar(self)
    self.costVariable = StringVar(self)
    self.totalCasesVariable = StringVar(self)
    
    Label(mainFrame, text="Time:").grid(row=2,column=1, sticky=(N,W,E,S))
    Label(mainFrame, textvariable=self.timeVariable).grid(row=2,column=2)
    Label(mainFrame, text="Depth:").grid(row=3,column=1, sticky=(N,W,E,S))
    Label(mainFrame, textvariable=self.depthVariable).grid(row=3,column=2)
    Label(mainFrame, text="Cost:").grid(row=4,column=1, sticky=(N,W,E,S))
    Label(mainFrame, textvariable=self.costVariable).grid(row=4,column=2)
    Label(mainFrame, text="# of Cases:").grid(row=5,column=1, sticky=(N,W,E,S))
    Label(mainFrame, textvariable=self.totalCasesVariable).grid(row=5,column=2)

    self.cancelButton = Button(mainFrame, text="cancel", command=self.cancel)
    self.cancelButton.grid(row=6,column=1, columnspan=3, sticky=(N,W,E,S))
    
  def solve(self, board, callback):
    def endCallback(game):
      callback(game)
    self.progressbar["value"] = 0
    self.progressbar["maximum"] = calcTotalCost(board)
    self.thread = Thread(target=PopUp._solve, args=(self, board, endCallback,))
    self.thread.start()
    
  def cancel(self):
    self.cancelButton["state"] = DISABLED
    if self.thread and self.thread.isAlive():
      self.canceled = True
      print("Solver Canceled")

  def _solve(owner, board, callback):
    owner.startTime = time()
    g = solve(board, isDone=owner.isDone)
    callback(g)

  def updateUI(self, game):
    self.numberOf += 1
    maximum = self.progressbar["maximum"]
    if game.cost > maximum:
      self.progressbar["value"] = 0
    else:
      self.progressbar["value"] = maximum - game.cost
    self.totalCasesVariable.set(str(self.numberOf))
    self.depthVariable.set(str(game.depth))
    self.costVariable.set(str(game.cost))
    self.update_idletasks()
    self.timeVariable.set(round(time() - self.startTime, 4))
    
  def isDone(self, game):
    self.updateUI(game)
    if game.isDone():
      self.cancelButton["state"] = DISABLED
    
    return self.canceled or game.isDone()
  
if __name__ == "__main__":
  ui = UI()

  

  def makeMovesTest():
    moves = ["DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT","DOWN","RIGHT","UP","LEFT"]
    ui.makeMoves(moves)
    
  #ui.root.after(600, makeMovesTest)
  
  
  ui.start()
