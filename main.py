import sys

from GraphCreation import graphCreation as gc


def main():
    treeCache = {}
    argv = sys.argv

    try:
        treeCache = gc.load_object("treeCache.pickle")
    except:
        print("making new treeCache obj")

    if argv[1] == "add":
        # try:
        keyword = ""
        for i in range(2, len(argv) - 1):
            keyword += " " + argv[i]
        keyword = keyword.strip()
        print(keyword)
        gc.makeTreeBreadthFirst(keyword, int(argv[len(argv) - 1]), treeCache)
        gc.save_object(treeCache, "treeCache.pickle")
    # except:
    # print("pattern is `main.py add <Page Name> <# of Pages to Add>`")
    elif argv[1] == "print":
        # try:
        keyword = ""
        for i in range(2, len(argv)):
            keyword += " " + argv[i]
        keyword = keyword.strip()
        try:
            treeCache[keyword].printSummary()
        except:
            print("Can't find a page `" + keyword + "`")
            print("Running a search. Possible pages:")
            gc.search(keyword, treeCache)
    # except:
    # print("pattern is `main.py print <Page Name>`")
    elif argv[1] == "search":
        gc.search(argv[2])
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


if __name__ == "__main__":
    main()
