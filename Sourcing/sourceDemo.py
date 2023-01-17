import source
import proximityTree
import os

def main():

  os.system('clear')


  print("Welcome to the source tree demo \n\n")
  
  # Below is a list of example sources, collected from the wikipedia page for Python:
  
  sourceList = getSourceList()

  # These sources haven't been filtered or grouped, so in order to do that, we build a proximity tree out of the sources:

  sourceTree = proximityTree.ProximityTree.createTree(sourceList)

  # A proximity tree is essenitally my own version of a k-d tree. The main difference is that a k-d tree only works with points in space, and my proximity tree works with any objects for which distance is defined, like sets or tuples. Essentially what this does is create a tree of sources where each source under each subtree is more similar to that tree's root than that root's sibling. This creates a nested Voronoi partitioning of the source space. TLDR; it organizes sources close to sources that they're similar to in a big tree. Creation is O(nlogn). 

  # However, proximity trees, like k-d trees, are very very expensive to balance. Balancing them is critical not only for performance, but also for output optimization: we want distinctions in our datasets that split the 

  # Because balancing the trees is really hard once they've been made, I made an algorithm that runs in O(nlogn) to presort the input list in such a way that when fed into the tree creation algorithm, it creates a balanced tree. This is done by finding "antipodes," or points that about as far apart as possible, and splitting the dataset around those antipodes. This doesn't minimize variance within sets (otherwise it would be a k-means clustering problem which is NP-hard) but it does WORK to minimize range. Absolute minimal range not guaranteed, but this runs fast.

  balancedSourceTree = proximityTree.ProximityTree.createTree(proximityTree.balanceOrderProxTree(sourceList))


  # Okay, so now that these trees have been created, we're that much closer to actually sorting these sources. What we need to do now is split these trees down into subtrees, which form a disjoint set of the original set of sources. Remember that subtrees are more closely clustered than their supertrees, so this is how we extract source clusters.

  # The actual algorithm to do this basically starts with a tree, splits it into two subtrees, then splits the subtree with the largest area into two more subtrees. It stops when these splits no longer minimize range that much.

  sourceTrees = proximityTree.splitMax(sourceTree)
  balancedSourceTrees = proximityTree.splitMax(balancedSourceTree)

  # And now we can compare the source trees for the unbalanced trees...

  print("Unbalanced Source Tree (No clear relation between children and parents 🥺)")
  for sourceTree in sourceTrees:
    sourceTree.print()

  print("")
  print("Balanced Source Tree (Sources are split into a category on python for cybersecurity and a category on python syntax and history 😁)")
  for sourceTree in balancedSourceTrees:
    sourceTree.print()

  print("\n")

  # We can confirm that the balanced tree is much better at source sorting by checking the area of each tree:

  print("Unbalanced Proximity Tree Area: %f" % (proximityTree.sumArea(sourceTrees, 2)))

  print("Balanced Proximity Tree Area: %f" % (proximityTree.sumArea(balancedSourceTrees, 2)))

  # The balanced tree has less, but it also has fewer subtrees. This is important as a smaller sum area is harder to achieve the fewer trees you have. Because of this, I like to compare the product of (number of trees * total area of trees), which is a statistic I call locality. Balanced trees have a much lower locality than unbalanced:

  print("\n")
  print("Unbalanced Trees Locality: %f" % proximityTree.getLocality(sourceTrees, 2))
  print("Balanced Trees Locality: %f" % proximityTree.getLocality(balancedSourceTrees, 2))



  # PS range is the term used here to mean the distance between the two farthest points. Area is range raised to some power. 

def getSourceList():
  return [
    source.Source("swift evolution process","",{
      "Swift": 11.2,
      "Evolution": 5.1,
      "Programming": 2.2,
      "Multiparadigm": 1.7,
      "Python": 1.0
    }),
    source.Source("mypy-- optional static typing for python","",{
      "Python": 12.3,
      "Typing": 11.1,
      "Version": 6.0,
      "Syntax": 4.0,
      "Programming": 1.2
    }),
    source.Source("why must ‘self’ be used explicitly in method definitions and calls?","",{
      "Python": 9.3,
      "Syntax": 8.1,
      "Self": 3.1,
      "Methods": 2.0,
    }),
    source.Source("why was python created in the first place?","",{
      "History": 12.2,
      "Python": 9.7,
      "Guido Van Rossum": 8.2,
      "Programming": 1.0
    }),
    source.Source("why is it called python?","",{
      "Monty Python": 9.2,
      "Python": 9.7,
      "History": 3.0,
      "Guido Van Rossum": 2.0
    }),
    source.Source("immunity: knowing you're secure","",{
      "Cybersecurity": 9.2,
      "Debugging": 5.1,
      "Hacking": 4.2,
      "Python": 1.1,
    }),
    source.Source("groovy- the birth of a new language for the java platform","",{
      "Groovy": 10.1,
      "Java": 5.2,
      "Dynamic": 5.1,
      "Syntax": 4.0,
      "Programming": 3.2,
      "Python": 1.1
    }),
    source.Source("how to use python for mitm attacks","",{
      "HTTP": 10.1,
      "Cybersecurity": 5.5,
      "Hacking": 4.2,
      "Python": 3.7
    }),
  ]

if __name__ == "__main__":
  main()