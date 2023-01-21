from Sourcing import source as src


class MapNode:
    def __init__(self, name, relatedNodes, summary, sources, id):
        self.name = name
        self.relatedNodes = relatedNodes
        self.summary = summary
        self.sources = sources
        self.id = id

    @staticmethod
    def fromTreeNode(tnode):
        sources = []
        for link in tnode.page.links:
            print(link)
            sources.append(src.Source("sourceName", link, []))
        return MapNode(tnode.name, [], tnode.page.summary, sources, tnode.page.pageid)

    def toConsole(self, indentLevel = 0):
        indent = "\t" * indentLevel
        clippedSummary = self.summary[:47] + "..." if len(self.summary) > 47 else ""
        print(indent + "- "+self.name+": " + clippedSummary)
        for relatedNode in self.relatedNodes:
            relatedNode.toConsole(indentLevel+1)
        pass
