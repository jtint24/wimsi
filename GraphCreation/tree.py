class Edge:
  def __init__(self, weight: float, target):
    self.weight = weight
    self.target = target

class Link:
  def __init__(self, name, weight):
    self.name = name
    self.weight = weight

class TreeNode:
  def __init__(self, name: str, edges, summary, sourceLinks, treeCache):
    self.name = name
    self.edges = edges
    self.summary = summary
    self.sourceLinks = sourceLinks
    treeCache[name] =  self
  def print(self):
    print(self.name)
    for edge in self.edges:
      print("\t-"+edge.target.name)
  def printSummary(self, w):
    print(self.name)
    print(self.summary)
    for edge in self.edges:
      print("\t-"+edge.target.name)
  def printI(self, depth):
    print("\t"*depth+"- "+self.name)
    for edge in self.edges.links:
      edge.target.printI(depth+1)