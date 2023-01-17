import pickle
import time
import wikipediaapi
from GraphCreation import priorityQueue as pq
from GraphCreation import tree as tr

# MINIMUM LINK FREQUENCY IN PAGE TO BE ADDED TO TREE
CT_THRESH = 2

# 1.28 seconds / node at 400
# 1.29 seconds / node at 500
# 1.35 seconds / node at 1000


wikipedia = wikipediaapi.Wikipedia('en')

pages = {}


def search(name, treeCache):
    for pname in treeCache.keys():
        if name in pname.lower():
            print(" - `" + pname + "`")


def load_object(filename):
    with open(filename, "rb") as input_file:
        return pickle.load(input_file)


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def makeTreeBreadthFirst(name: str, count: int, treeCache):
    nodeQueue = pq.PriorityQueue([name])
    i = 0

    initialText = getPage(name).text
    start_time = time.time()
    while i < count and not nodeQueue.length() == 0:
        popped = nodeQueue.pop()
        nameToMakeFrom = popped.obj
        print("%d #%s/%s:\t %s %s" % (time.time() - start_time, i, nodeQueue.length(), nameToMakeFrom, popped.priority))

        page = getPage(nameToMakeFrom)

        links = getLinks(nameToMakeFrom)

        if nameToMakeFrom not in treeCache.keys():
            treeCache[nameToMakeFrom] = tr.TreeNode(nameToMakeFrom, [], page, treeCache)

        for link in links:
            if (link.name not in nodeQueue.toList()) and (link.name not in treeCache.keys()):
                nodeQueue.priorityInsert(link.name, initialText.count(link.name))

        for link in links:
            if link.name not in treeCache.keys():
                treeCache[link.name] = tr.TreeNode(link.name, [], getPage(link.name), treeCache)
            treeCache[nameToMakeFrom].edges.append(tr.Edge(link.weight, treeCache[link.name]))

        i += 1


def getLinks(pageName: str) -> [str]:
    global CT_THRESH
    try:
        page = getPage(pageName)
    except:
        return []
    links = list(set(page.links))
    text = page.text
    filteredLinks = []

    # sort links by count and filter out uncommon ones
    for link in links:
        count = text.count(link)
        if count >= CT_THRESH:
            insIdx = 0
            while insIdx < len(filteredLinks) and filteredLinks[insIdx][0] > count:
                insIdx += 1
            filteredLinks.insert(insIdx, [count, link])

    filteredLinks = list(map(lambda linkPair: tr.Link(linkPair[1], linkPair[0]), filteredLinks))

    return filteredLinks


def getPage(name):
    if name not in pages:
        pages[name] = wikipedia.page(name)
    return pages[name]
