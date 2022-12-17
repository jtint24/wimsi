import sys, wikipedia, time
import  pickle


# MINIMUM LINK FREQUENCY IN PAGE TO BE ADDED TO TREE
CT_THRESH = 2

# 1.28 seconds / node at 400
# 1.29 seconds / node at 500
# 1.35 seconds / node at 1000

treeCache = {}

def main():
  global treeCache
  argv = sys.argv

  treeCache = load_object("treeCache.pickle")
  
  if argv[1] == "add":
    keyword = ""
    for i in range(2, len(argv)-1):
      keyword += " "+argv[i]
    keyword = keyword.strip()
    print(keyword)
    makeTreeBreadthFirst(keyword, int(argv[len(argv)-1]))
    save_object(treeCache, "treeCache.pickle")
  elif argv[1] == "print":
    keyword = ""
    for i in range(2, len(argv)):
      keyword += " "+argv[i]
    keyword = keyword.strip()
    try:
      treeCache[keyword].printSummary()
    except:
      print("Can't find a page `"+keyword+"`")
      print("Running a search. Possible pages:")
      search(keyword)
  elif argv[1] == "search":
    search(argv[2])
  elif argv[1] == "stats":
    print("TreeCache stats:")
    print("number of nodes: %s" % (len(treeCache)))
    nonBlankCount = 0
    for tree in treeCache.values():
      if len(tree.edges) != 0:
        nonBlankCount += 1
    print("number of trees: %s" % (nonBlankCount))

  else:
    print("command not found, run: main.py <add|search|print|stats>")
  
  #makeTreeBreadthFirst("Python_(Programming_language)", 10)
  #for tree in treeCache.values():
    #tree.print()
  
  pass

def search(name):
  for pname in treeCache.keys():
    if name in pname.lower():
      print(" - `"+pname+"`")

def load_object(filename):
  with open(filename, "rb") as input_file:
    return pickle.load(input_file)

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def makeTreeBreadthFirst(name: str, count: int):
  global treeCache
  nodeQueue = PriorityQueue([name])
  i = 0
  initialText = wikipedia.page(name).content
  start_time = time.time()
  while i<count and not nodeQueue.length()==0:
    popped = nodeQueue.pop()
    nameToMakeFrom = popped.obj
    print("%d  #%s/%s:\t %s %s" % (time.time() - start_time, i, nodeQueue.length(), nameToMakeFrom, popped.priority))


    links = getLinks(nameToMakeFrom)

    if (not nameToMakeFrom in treeCache.keys()):
      treeCache[nameToMakeFrom] = TreeNode(nameToMakeFrom, [])

    for link in links:
      if (not link.name in nodeQueue.toList()) and (not link.name in treeCache.keys()):
        nodeQueue.priorityInsert(link.name, initialText.count(link.name))

    for link in links:
      if not link.name in treeCache.keys():
        treeCache[link.name] = TreeNode(link.name, [])
      treeCache[nameToMakeFrom].edges.append(Edge(link.weight, treeCache[link.name]))

    i+=1

  

def getLinks(pageName: str) -> [str]:
  global thresh
  try:
    page = wikipedia.page(pageName)
  except:
    return []
  links = list(set(page.links))
  text = page.content
  filteredLinks = []

  # sort links by count and filter out uncommon ones
  for link in links:
    count = text.count(link)
    if count >= CT_THRESH:
      insIdx = 0
      while insIdx<len(filteredLinks) and filteredLinks[insIdx][0] > count:
        insIdx+=1
      filteredLinks.insert(insIdx, [count, link])

  filteredLinks  = list(map(lambda linkPair: Link(linkPair[1], linkPair[0]), filteredLinks))

  return  filteredLinks

  
class Edge:
  def __init__(self, weight: float, target):
    self.weight = weight
    self.target = target

class Link:
  def __init__(self, name, weight):
    self.name = name
    self.weight = weight

class TreeNode:
  def __init__(self, name: str, edges):
    global treeCache
    self.name = name
    self.edges = edges
    treeCache[name] =  self
  def print(self):
    print(self.name)
    for edge in self.edges:
      print("\t-"+edge.target.name)
  def printSummary(self):
    print(self.name)
    print(wikipedia.page(self.name).summary)
    for edge in self.edges:
      print("\t-"+edge.target.name)
  def printI(self, depth):
    print("\t"*depth+"- "+self.name)
    for edge in self.edges.links:
      edge.target.printI(depth+1)

class PriorityQueueNode:
  def __init__(self, obj, priority):
    self.obj = obj
    self.priority = priority

# TODO: Make this a heap

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
  
if __name__ == "__main__":
  main()