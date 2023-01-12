import math
import source

class ProximityTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.sra = 0
    def range(self):
        return self.sra
    def createTree(values):
        newTree = ProximityTree(values[0])
        for node in values[1:]:
            newTree.insert(ProximityTree(node))
        return newTree
    def insert(self, node):
        dis = distance(node.value, self.value)
        if dis > self.sra:
            self.sra = dis
        if self.left == None:
            self.left = node
            return
        if self.right == None:
            self.right = node
            return
        if distance(self.left.value, node.value) < distance(self.right.value, node.value):
            self.left.insert(node)
        else:
            self.right.insert(node)
    def print(self, tab = 0):
        print("  "*tab + "- "+str(self.value))
        if self.left != None:
            self.left.print(tab+1)
        if self.right != None:
            self.right.print(tab+1)
    def height(self):
        leftHeight = 0
        rightHeight = 0
        if self.left == None:
            leftHeight = 0
        else:
            leftHeight = self.left.height()
        if self.right == None:
            rightHeight = 0
        else:
            rightHeight = self.right.height()
        return max(leftHeight, rightHeight)+1
    def size(self):
        leftSize = 0
        rightSize = 0
        if self.left == None:
            leftSize = 0
        else:
            leftSize = self.left.size()
        if self.right == None:
            rightSize = 0
        else:
            rightSize = self.right.size()
        return rightSize+leftSize+1
    def split(self):
        newNode = ProximityTree(self.value)
        if self.left == None:
            self.right.insert(newNode)
            return [self.right]
        if self.right == None:
            self.left.insert(newNode)
            return [self.left]
        if distance(newNode.value, self.right.value) < distance(newNode.value, self.left.value):
            self.right.insert(newNode)
        else:
            self.left.insert(newNode)
        return [self.left, self.right]
    def printCSV(self):
        printCSV(self.value)
        if self.left != None:
            self.left.printCSV()
        if self.right != None:
            self.right.printCSV()


def printCSV(vec):
    for i in vec[0:len(vec)-1]:
        print(i, end=", ")
    print(vec[len(vec)-1])
    
def distance(A, B):
    sqSum = 0
    for (a,b) in zip(A,B):
        sqSum = (a-b)**2
    return math.sqrt(sqSum)
    
def balanceOrderProxTree(values):
    # print("balancing "+str(values))
    if len(values) == 0:
        return []
    meanPoint = getMeanPoint(values)
    centralPoint = getClosestTo(meanPoint, values)
    # print("centralPoint: "+str(centralPoint))
    values.remove(centralPoint)
    retList = [centralPoint]
    if len(values) > 1:
        antipodeA = getFarthestFrom(centralPoint, values)
        values.remove(antipodeA)
        antipodeB = getFarthestFrom(antipodeA, values)
        values.remove(antipodeB)
        
        # print("enough for antipodes: "+str(antipodeA)+" "+str(antipodeB))

        
        (closestToA, closestToB) = proximityPartition(antipodeA, antipodeB, values)
        # print("closest to A: "+str(closestToA))
        # print("closest to B: "+str(closestToB))
        
        closestToA.insert(0,antipodeA)
        closestToB.insert(0,antipodeB)
        
        balancedA = balanceOrderProxTree(closestToA)
        balancedB = balanceOrderProxTree(closestToB)

        return retList + [balancedA[0]] + [balancedB[0]] + balancedA[1:] + balancedB[1:]
    else:
        retList += values
        # print("not enough for antipodes: "+str(values))
        return retList
        
def getFarthestFrom(point, values):
    maxDistance = distance(values[0], point)
    farthestPoint = values[0]
    for value in values[1:]:
        dis = distance(value, point)
        if (distance(value, point) > maxDistance):
            maxDistance = dis
            farthestPoint = value
    return farthestPoint
            
def getClosestTo(point, values):
    minDistance = distance(values[0], point)
    closestPoint = values[0]
    for value in values[1:]:
        dis = distance(value, point)
        if (distance(value, point) < minDistance):
            minDistance = dis
            closestPoint = value
    return closestPoint
    
def getMeanPoint(values):
    point = [0] * len(values[0])
    for value in values:
        for i in range(len(value)):
            point[i] += value[i]
    for i in range(len(point)):
        point[i] /= len(values)
    return point
    
def proximityPartition(antipodeA, antipodeB, values):
    closestToA = []
    closestToB = []
    for value in values:
        if (distance(antipodeA, value) < distance(antipodeB, value)):
            closestToA.append(value)
        else:
            closestToB.append(value)
            
    return (closestToA, closestToB)
    


def splitMax(tree):
    dim = len(tree.value)
    oldArea = tree.range()**dim
    trees = tree.split()
    maxRangeTree = getMaxRangeTree(trees)
    while True:
        oldArea = sumArea(trees, dim)
        splitTrees = maxRangeTree.split()
        if splitTrees == None:
            break
        for tree in trees:
            if tree != maxRangeTree:
                splitTrees.insert(0, tree)
        if sumArea(splitTrees, dim) >= oldArea:
            break
        trees = splitTrees
        maxRangeTree = getMaxRangeTree(trees)
    return trees

def getMaxRangeTree(trees):
    mrangeTree = None
    mrange = 0
    for tree in trees:
        if tree.size() > 3:
            if mrange < tree.range():
                mrange = tree.range()
                mrangeTree = tree
    return mrangeTree

def sumArea(trees, dim):
    sum = 0
    for tree in trees:
        sum += tree.range()**dim
    return sum


def main():

    points = []
    for i in range(200):
        points += [[math.sin(i)*i, math.cos(i)*i]]
    tree = ProximityTree.createTree(points)
    points = balanceOrderProxTree(points)
    balancedTree = ProximityTree.createTree(points)
    
    trees = splitMax(tree)
    balancedTrees = splitMax(balancedTree)    
    print("unbalanced tree | sum area: "+str(sumArea(trees,2))+" num trees: "+str(len(trees)))
    print("balanced tree   | sum area: "+str(sumArea(balancedTrees,2))+" num trees: "+str(len(balancedTrees)))


if __name__ == "__main__":
  main()