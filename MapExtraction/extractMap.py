
from GraphCreation import priorityQueue as pq

SIMILARITY_THRESH = .1
def extractMap(treeCache, name):
    global SIMILARITY_THRESH

    rootNode = treeCache[name]
    queue = pq.PriorityQueue([rootNode])

    while queue.length != 0:
        node = queue.pop()

        for link in node.edges:
            target = link.target
            similarity = pageSimilarity(target.page, rootNode.page)
            if similarity > SIMILARITY_THRESH:
                queue.priorityInsert(target, similarity)

def pageSimilarity(pageA, pageB):
    return 1




