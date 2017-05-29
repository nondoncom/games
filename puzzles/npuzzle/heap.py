

class Heap(object):
  def __init__(self, checkParent):
    self.data = []
    self.checkParent = checkParent
  
  def size(self):
    return len(self.data)
  
  def empty(self):
    return self.size() == 0
    
  def put(self, object):
    self.data.append(object)
    self.__bubbleUp(len(self.data)-1)

  def get(self):
    return self.getFrom(0)
    
  def getFrom(self, index):
    size = len(self.data)
    if index < size and index >= 0:
      value = self.data[index]
      self.__swap(index, size-1)
      del self.data[size-1]
      if index != 0 and index != size-1:
        self.__bubbleUp(index)
      self.__bubbleDown(index)
      return value
    return None
  
  def __swap(self, i, j):
    self.data[i], self.data[j] = self.data[j], self.data[i]
  
  def __children(index):
    if index == 0:
      return (1,2)
    return (((index+1)*2)-1, ((index+1)*2))
  
  def __parent(index):
    return (index-1)//2
  
  def __bubbleUp(self, index):
    while index != 0:
      parent = Heap.__parent(index)
      if self.checkParent(self.data[index], self.data[parent]):
        self.__swap(index, parent)
        index = parent
      else:
        break
      
  def __bubbleDown(self, index):
    size = len(self.data)
    if index >= size or index < 0:
      return
    children = Heap.__children(index)
    while(children[0]<size):    
      if (
          (
            children[1] >= size or 
            self.checkParent(self.data[children[0]], self.data[children[1]])
          ) and 
          self.checkParent(self.data[children[0]], self.data[index])
         ):
        self.__swap(index, children[0])
        index = children[0]
      elif (
            children[1] < size and
            self.checkParent(self.data[children[1]], self.data[children[0]]) and 
            self.checkParent(self.data[children[1]], self.data[index])
           ):
        self.__swap(index, children[1])
        index = children[1]
      else:
        break
      children = Heap.__children(index)
        
  def __str__(self):
    value = ""
    k = 2
    for i, d in enumerate(self.data):
      if i+1 >= k:
        value += "\n"
        k = k * 2
      value += str(d) + " "
    return value
    
class MaxHeap(Heap):
  def __init__(self):
    def maxf(parent, child):
      return not parent < child
    Heap.__init__(self,maxf)
    
class MinHeap(Heap):
  def __init__(self):
    def minf(parent, child):
      return not parent > child
    Heap.__init__(self,minf)
    
if __name__ == '__main__':
  
  size = 20
  def fillHeap(heap, size):
    for i in range(size):
      heap.put(i)
      
  def test(minMax, testf):
    heap = minMax()
    fillHeap(heap,size)
    print(heap)
    for i in range(size):
      d = heap.get()
      assert testf(d,i), "Not Equal"
      print("Removed ", d, "\n")
      print(heap)
      
  def minf(parent, child):
    return parent <= child
  def minTest(d,i):
    return d == i
    
  def maxf(parent, child):
    return parent >= child
  def maxTest(d,i):
    return d == (size - 1 - i)
  
  print("Test Min")
  test(MinHeap,minTest)
  
  print("Test Max")
  test(MaxHeap,maxTest)
  
  print("MinHeap: Test Duplicate")
  heap = MinHeap()
  heap.put(1)
  heap.put(2)
  heap.put(1)
  heap.put(3)
  heap.put(1)
  heap.put(4)
  heap.put(1)
  heap.put(5)
  heap.put(1)
  heap.put(2)
  heap.put(1)
  print(heap)
  for i in range(6):
    d = heap.get()
    assert d == 1, "Not Equal to 1"
  print(heap)
  for i in range(2):
    d = heap.get()
    assert d == 2, "Not Equal to 2"
  print(heap)
  d = heap.get()
  assert d == 3, "Not Equal to 3"
  d = heap.get()
  assert d == 4, "Not Equal to 4"
  d = heap.get()
  assert d == 5, "Not Equal to 5"
  
  
  print("MaxHeap: Test Duplicate")
  heap = MaxHeap()
  heap.put(1)
  heap.put(2)
  heap.put(1)
  heap.put(3)
  heap.put(1)
  heap.put(4)
  heap.put(1)
  heap.put(5)
  heap.put(1)
  heap.put(2)
  heap.put(1)
  print(heap)
  d = heap.get()
  assert d == 5, "Not Equal to 5"
  d = heap.get()
  assert d == 4, "Not Equal to 4"
  d = heap.get()
  assert d == 3, "Not Equal to 3"
  print(heap)
  for i in range(2):
    d = heap.get()
    assert d == 2, "Not Equal to 2"
  print(heap)
  for i in range(6):
    d = heap.get()
    assert d == 1, "Not Equal to 1"
  
  print("MinHeap: Test reove at index")
  heap = MinHeap()
  fillHeap(heap, 20)
  print(heap)
  d = heap.getFrom(5)
  assert d == 5, "Not Equal to 5"
  print(heap)
  d = heap.getFrom(5)
  assert d == 11, "Not Equal to 11"
  for i in range(0,5):
    d = heap.get()
    assert minTest(d,i), "Not Equal:"+str(i)
  for i in range(6,11):
    d = heap.get()
    assert minTest(d,i), "Not Equal:"+str(i)
  for i in range(12,20):
    d = heap.get()
    assert minTest(d,i), "Not Equal:"+str(i)

  print("MaxHeap: Test reove at index")
  heap = MaxHeap()
  fillHeap(heap, 20)
  print(heap)
  d = heap.getFrom(5)
  assert d == 10, "Not Equal to 10"
  print(heap)
  d = heap.getFrom(5)
  assert d == 5, "Not Equal to 5"
  for i in range(0,9):
    d = heap.get()
    assert maxTest(d,i), "Not Equal:"+str(i)
  for i in range(10,14):
    d = heap.get()
    assert maxTest(d,i), "Not Equal:"+str(i)
  for i in range(15,20):
    d = heap.get()
    assert maxTest(d,i), "Not Equal:"+str(i)
  