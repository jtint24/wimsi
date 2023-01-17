
# Wrote my own priority queue lol, couldn've imported something but I just didn't
# TODO: Make this a heap

class PriorityQueueNode:
  def __init__(self, obj, priority):
    self.obj = obj
    self.priority = priority

class PriorityQueue:
  def __init__(self, contents):
    self.contents = []
    for contentNode in contents:
      self.contents.append(PriorityQueueNode(contentNode, 100))
  def toList(self):
    return list(map(lambda node: node.obj, self.contents))
  def length(self):
    return len(self.contents)
  def pop(self):
      return self.contents.pop(0)
  def priorityInsert(self, node, priority):
    if priority == 0:
      self.contents.append(PriorityQueueNode(node, priority))
      return
    for i in range(0, len(self.contents)):
      queueNode = self.contents[i]
      if queueNode.priority < priority:
        self.contents.insert(i, PriorityQueueNode(node, priority))
        return
    self.contents.append(PriorityQueueNode(node, priority))