import time
import requests

class WikipediaPage:
    def __init__(self, title, pageid, summary, text, links, canonicalUrl):
        self.title = title
        self.pageid = pageid
        self.summary = summary
        self.text = text
        self.links = links
        self.canonicalUrl = canonicalUrl
        self.accessTime = time.time()

        try:
            r = requests.get("https://en.wikipedia.org/w/api.php?action=parse&page="+title+"&prop=externallinks&format=json")
            r.raise_for_status()
            self.references = r.json()["parse"]["externallinks"]
        except:
            self.references = []


    @staticmethod
    def fromPage(page):
        return WikipediaPage(page.title, page.pageid, page.summary, page.text, page.links, page.canonicalurl)
