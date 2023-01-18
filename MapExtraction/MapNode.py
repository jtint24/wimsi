class MapNode:
    def __init__(self, name, relatedNodes, summary, sources):
        self.name = name
        self.relatedNodes = relatedNodes
        self.summary = summary
        self.sources = sources

    @staticmethod
    def fromTreeNode(tnode):
        return MapNode(tnode.name, [], tnode.page.summary[:1], [])
        pass
