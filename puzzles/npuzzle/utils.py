
def _merge(board, start, mid, end):
  data = [0] * (end - start)
  i = start
  j = mid
  count = 0
  for k in range(len(data)):
    if j < end:
      if i < mid and board[i]<=board[j]:
        data[k] = board[i]
        i+=1
      else:
        data[k] = board[j];
        j+=1
        count += (mid - i);
    else:
      if i < mid:
        data[k] = board[i]
        i+=1
  k = 0
  i = start
  for k in range(len(data)):
      board[i] = data[k]
      i+=1
  
  return count

def mergeCount(board, start, end):
  count = 0
  if (end-start) > 1:
    mid = (start+end) // 2
    left = mergeCount(board, start, mid)
    right = mergeCount(board, mid, end)
    merge = _merge(board, start, mid, end)
    count = left + right + merge
  return count


def manhattanDistance(pos1, pos2):
  return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def euclideanDistance(pos1, pos2):
  return math.sqrt(pow(pos1[0]-pos2[0],2)+pow(pos1[1]-pos2[1],2))
  
def swap(metrix, p1, p2):
  metrix[p1[0]][p1[1]], metrix[p2[0]][p2[1]] = metrix[p2[0]][p2[1]], metrix[p1[0]][p1[1]]
  return metrix
  
  
if __name__ == "__main__":
  testList = [6,13,7,10,8,9,11,15,2,12,5,14,3,1,4]
  count = mergeCount(testList,0,len(testList))
  print(count)
  assert(count == 62)
  testList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
  count = mergeCount(testList,0,len(testList))
  print(count)
  assert(count == 0)
  testList = [7,6,5,4,3,2,1]
  count = mergeCount(testList,0,len(testList))
  print(count)
  assert(count == 21)