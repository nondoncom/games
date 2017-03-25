
import copy
import math
from utils import manhattanDistance, swap


class NPuzzle():
  def __init__(self, board, zero=None, cost=0, depth=0, moves=[]):
    self.board = copy.deepcopy(board)
    if zero != None:
      self.zero = copy.deepcopy(zero)
    else:
      self.zero = NPuzzle.findZero(board)
    self.cost = cost
    self.depth = depth
    self.size = len(board)
    self.moves = copy.deepcopy(moves)
    self.bStart = 0

  def __lt__(self, other):
    #return (self.cost+self.depth) < (other.cost+other.depth)
    return ((self.bStart < other.bStart) or ((self.bStart == other.bStart) and (self.cost+self.depth) < (other.cost+other.depth)))
    #return (self.cost) < (other.cost)
  
  def __str__(self):
    return str(self.board)

  __moves = [(1,0,"UP"),(0,-1,"RIGHT"),(-1,0,"DOWN"),(0,1,"LEFT")]
  def _getMoves(pos, S, E):
    return [ x for x in [(pos[0]+v[0], pos[1]+v[1], v[2]) for v in NPuzzle.__moves] if x[0]>=S and x[0]<E and x[1]>=S and x[1]<E ]
  
  def isLegal(self, pos):
    return manhattanDistance(self.zero, pos) == 1
    
  def findActualPosition(value, N):
    actVal = value - 1
    pos = ((actVal // N), (actVal % N))
    return pos

  def findZero(board):
    N = len(board)
    return [(r,c) for r in range(N) for c in range(N) if board[r][c] == 0][0]
    
  def move(self, pos):
    if self.isLegal(pos):
      swap(self.board, self.zero, pos)
      self.zero = pos
      if min(pos[0],pos[1]) == self.bStart:
        self._updateBoundry()
      return True
    return False
    
  def _updateBoundry(self):
    isGood = True
    if self.size - self.bStart > 3:
      for i in range(self.bStart, self.size):
        if (i, self.bStart) != NPuzzle.findActualPosition(self.board[i][self.bStart], self.size):
          isGood = False
          break
      if isGood:
        for j in range(self.bStart+1, self.size):
          if (self.bStart, j) != NPuzzle.findActualPosition(self.board[self.bStart][j], self.size):
            isGood = False
            break
      if isGood:
        self.bStart += 1
        #print("Up boundary:", self.bStart)
    
  def getPosibleMoves(self):
    return NPuzzle._getMoves(self.zero, self.bStart, self.size)

  def isDone(self):
    return self.cost == 0


if __name__ == "__main__":
  pos = NPuzzle.findActualPosition(1, 4)
  print(pos)
  assert(pos == (0,0))
  pos = NPuzzle.findActualPosition(4, 4)
  print(pos)
  assert(pos == (0,3))
  pos = NPuzzle.findActualPosition(13, 4)
  print(pos)
  assert(pos == (3,0))
  pos = NPuzzle.findActualPosition(15, 4)
  print(pos)
  assert(pos == (3,2))
  
  moves = NPuzzle._getMoves((0,0), 0, 2)
  print(moves)
  assert(moves == [(1,0,'DOWN'),(0,1,'RIGHT')])
  moves = NPuzzle._getMoves((1,1), 0, 4)
  print(moves)
  assert(moves == [(2,1,'DOWN'),(1,2,'RIGHT'),(0,1,'UP'),(1,0,'LEFT')])
  moves = NPuzzle._getMoves((1,1), 0, 2)
  print(moves)
  assert(moves == [(0,1,'UP'),(1,0,'LEFT')])