import time


class WikipediaPage:
    def __init__(self, title, pageid, summary, text, links):
        self.title = title
        self.pageid = pageid
        self.summary = summary
        self.text = text
        self.links = links
        self.accessTime = time.time()

    @staticmethod
    def fromPage(page):
        return WikipediaPage(page.title, page.pageid, page.summary, page.text, page.links)
