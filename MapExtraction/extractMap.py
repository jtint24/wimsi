import random

from GraphCreation import priorityQueue as pq
from MapExtraction import mapNode as mn

SIMILARITY_THRESH = .7


def extractMap(treeCache, name):
    global SIMILARITY_THRESH

    rootTNode = treeCache[name]
    rootMNode = mn.MapNode.fromTreeNode(rootTNode)
    queue = pq.PriorityQueue([(rootTNode, rootMNode)])

    nodeSize = 0
    addedNodeIDs = [rootTNode.page.pageid]
    while queue.length != 0 and nodeSize < 100:
        if len(queue.contents) == 0:
            break

        (tnode, mnode) = queue.pop().obj

        for edge in tnode.edges:
            target = edge.target

            if target.page.pageid in addedNodeIDs:
                continue

            similarity = pageSimilarity(target.page, rootTNode.page)

            if similarity > SIMILARITY_THRESH:
                tnodeToAdd = target
                mnodeToAdd = mn.MapNode.fromTreeNode(tnodeToAdd)
                queue.priorityInsert((tnodeToAdd, mnodeToAdd), similarity)
                mnode.relatedNodes.append(mnodeToAdd)
                addedNodeIDs.append(tnodeToAdd.page.pageid)

                nodeSize += 1
    print("created " + str(nodeSize) + " nodes")
    return rootMNode


def pageSimilarity(pageA, pageB):
    return random.randint(0, 10) / 10
