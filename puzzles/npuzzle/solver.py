
from random import randint
from queue import PriorityQueue
import time

from utils import * 
from puzzle import NPuzzle

def _countInversions(board):
  """
  Count inversions
  """
  boardList = [board[r][c] for r in range(len(board)) for c in range(len(board)) if board[r][c] != 0]
  return mergeCount(boardList,0,len(boardList))

def isSolvable(board):
  """
  check if puzzle can be solved
  """
  N = len(board)
  inversionCount = _countInversions(board)
  if N%2 == 1:
    return inversionCount%2==0
  else:
    zeroRaw = NPuzzle.findZero(board)
    if (N - zeroRaw[0])%2 == 0:
      return inversionCount%2 == 1
    else:
      return inversionCount%2 == 0


def _getDistance(pos1, pos2):
  return manhattanDistance(pos1, pos2)
  #return euclideanDistance(pos1, pos2)
  
def _calcCost(pos, value, N):
  """
  Calculate tile cost
  Using distance and layer of a tile as heuristic.
  Addition of layer makes it a sub optimal solution.
  """
  actPos = NPuzzle.findActualPosition(value, N)
  return (N - min(actPos[0],actPos[1])) * _getDistance(pos, actPos)

def _calcMoveCost(fromPos, toPos, value, N):
  return (_calcCost(toPos, value, N) - _calcCost(fromPos, value, N))
  #return (_calcCost(fromPos, value, N) - _calcCost(toPos, value, N))

def calcTotalCost(board, bStart=0):
  N = len(board)
  cost = sum([_calcCost((x,y),board[x][y],N) for x in range(bStart, N) for y in range(bStart, N) if board[x][y] != 0 ])
  return cost
    
def solve(board, 
          isDone=lambda game: game.isDone(), 
          costOfMove=lambda fromP, toP, game: _calcMoveCost(fromP, toP, game.board[fromP[0]][fromP[1]], game.size),
          totalCost=calcTotalCost,
          maxDepth = 0):
  """
  A* search to finde solution
  """
  boards = set()
  puzzles = PriorityQueue()
  zeroPos = NPuzzle.findZero(board)
  npuzzle = NPuzzle(board,zeroPos,0)
  npuzzle.cost = totalCost(npuzzle.board)
  puzzles.put(npuzzle)
  searchMaxDepth = 0
  while not puzzles.empty():
    npuzzle = puzzles.get()
    
    if searchMaxDepth < npuzzle.depth:
      searchMaxDepth = npuzzle.depth
      print(searchMaxDepth, npuzzle.cost, puzzles.qsize())
      
    if isDone(npuzzle):
      return npuzzle

    #print(npuzzle, npuzzle.cost, npuzzle.depth, puzzles.qsize())

    if maxDepth > 0 and maxDepth < npuzzle.depth:
      continue
        
    currentMoves = npuzzle.getPosibleMoves()
    currentMoves = [ (costOfMove(fromP, npuzzle.zero, npuzzle), fromP) for fromP in currentMoves ]
    
    #currentMoves = sorted(currentMoves, key=lambda x: x[0])
    #print(currentMoves)
    for i, move in enumerate(currentMoves):
      #if i > 0 and move[0] > 0:
      #  rand = randint(10, 200)
      #  if rand < npuzzle.depth: 
      #    continue

      zeroPos = npuzzle.zero
      npuzzle.move(move[1])
      strRepresentation = str(npuzzle.board)
      if strRepresentation not in boards:
        boards.add(strRepresentation)
        newPuzzle = NPuzzle(npuzzle.board,move[1],npuzzle.cost+move[0],npuzzle.depth+1,npuzzle.moves+[move[1][2]])
        newPuzzle.bStart = npuzzle.bStart
        newPuzzle.cost = totalCost(newPuzzle.board, newPuzzle.bStart)
        puzzles.put(newPuzzle)
      npuzzle.move(zeroPos)
  #print("DONE!")
  return npuzzle

def genRandomBoard(N):
  board = []
  for i in range(N):
    board.append([0]*N)
  
  for x in range(1, N*N):
    r = randint(0,N-1)
    c = randint(0,N-1)
    count = 0
    while board[r][c] != 0:
      if count % 2 == 0:
        r+=1
      else:
        c+=1
      if r >= N or c >= N:
        r = randint(0,N-1)
        c = randint(0,N-1)
      count+=1
    board[r][c] = x

  return board


##############################################################
###########################TESTS##############################
##############################################################
def __tests():
  testBoard = [[6,13,7,10],
               [8,9,11,0],
               [15,2,12,5],
               [14,3,1,4]]
  count = _countInversions(testBoard)
  print(testBoard)
  print(count)
  assert(count == 62)

  solvable = isSolvable(testBoard)
  print(testBoard)
  print(solvable)
  assert(solvable)

  testBoard = [[3,9,1,15],
               [14,11,4,6],
               [13,0,10,12],
               [2,7,8,5]]
  solvable = isSolvable(testBoard)
  print(testBoard)
  print(solvable)
  assert(not solvable)

  dist = _getDistance((1,5),(2,4))
  print(dist)
  assert(dist == 2)
  dist = _getDistance((1,5),(-1,-5))
  print(dist)
  assert(dist == 12)
  
  cost = _calcCost((3,3),1,4)
  print(cost)
  assert(cost == 24)
  cost = _calcCost((0,0),15,4)
  print(cost)
  assert(cost == 10)

def __createBoard(N):
  board = []
  for i in range(N):
    board.append([])
    for j in range(N):
      board[i].append(i*N+j+1)
  board[N-1][N-1] = 0
  return board

def __testSolver(testBoard):
  if isSolvable(testBoard):
    print(testBoard)
    finalBoard = __createBoard(len(testBoard))
    #print(finalBoard)
    print("Searching...")
    start = time.time()
    npuzzle = solve(testBoard)
    end = time.time()
    print("It took:", end-start, "sec")
    print(npuzzle.board)
    print(npuzzle.cost, npuzzle.depth, len(npuzzle.moves))
    #print(npuzzle.moves)
    assert(len(npuzzle.moves) > 0)
    assert(finalBoard == npuzzle.board)
    return (end-start, len(npuzzle.moves))
  else:
    print("Not Solvable")
    return (-1,0)
    
    
def __testPreSet():  
  testBoard =[
    [8, 7, 6],
    [5, 4, 3],
    [2, 1, 0]]

  testBoard = [
    [6,13,7,10],
    [8,9,11,0],
    [15,2,12,5],
    [14,3,1,4]]
    
  testBoard = [
    [6,13,7,10,16],
    [8,9,11,0,17],
    [15,2,12,5,18],
    [14,3,1,4,19],
    [20,24,22,23,21]]    

  testBoard = [
    [6,13,7,10,16,25],
    [8,9,11,0,17,26],
    [15,2,12,5,18,27],
    [14,3,1,4,19,28],
    [20,33,34,35,21,29],
    [30,24,22,23,31,32]]    

  testBoard = [[6, 7, 3], [0, 2, 4], [8, 1, 5]]  
  
  __testSolver(testBoard)    

if __name__ == "__main__":
  __tests()
  __testPreSet()
 
  average = (0,0)
  i = 0
  testCount = 1
  while i < testCount:
    testv = __testSolver(genRandomBoard(3))
    if testv[0] > 0:
      average = tuple(map(lambda a, b: a+b, testv, average))
      i+=1
  print("Average:", list(map(lambda a: a/testCount, average)), "for", testCount, "tests")

