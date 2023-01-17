import sys

class Source:
  def __init__(self, name, url, keywords):
    self.name = name
    self.url = url
    self.keywords = keywords
  def getDistanceTo(self, sourceB):

    # This is basic, basic, BASIC Jaccard distance. Replace with weighted cosine dist.
    
    unionSize = 0
    intersectionSize = 0

    for keyword in self.keywords:
      if not keyword in sourceB.keywords:
        unionSize += self.keywords[keyword]
      else:
        intersectionSize += self.keywords[keyword] + sourceB.keywords[keyword]
    for keyword in sourceB.keywords:
      unionSize += sourceB.keywords[keyword]

    if intersectionSize == 0:
      return sys.maxsize * 2 + 1
    return unionSize/intersectionSize
  def getCredibilityScore(self):
    return 0
  def getDimension(self):
    return 2
  def toString(self):
    return self.name
  