from . import BaseExtractor


class Nekonime(BaseExtractor):
    host = "https://nekonime.stream"
    tag = "anime"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        d = {}
        if (eps := soup.find(class_="daftarepi")):
            for a in eps.findAll("a"):
                d[a.text] = "re:" + self.getPath(a["href"])
            return d

        if (eps := soup.find(class_="flircontainer")):
            alleps = eps.find("a", text="All Eps")
            d[alleps.text] = "re:" + self.getPath(alleps["href"])

        if (ddl := soup.find(class_="soraddl")):
            for p in ddl.findAll(class_="soraurl"):
                result = {}
                for a in p.findAll("a"):
                    result[a.text] = a["href"]
                d[p.strong.text] = result
        return d

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={"s": query})
        soup = self.soup(raw)

        result = []
        for article in soup.findAll(class_="article-body"):
            a = article.find("a")
            result.append({
                "title": a.text,
                "id": self.getPath(a["href"])
            })
        return result
