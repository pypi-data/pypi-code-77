from . import BaseExtractor


class Kusonime(BaseExtractor):
    tag = "anime"
    host = "https://kusonime.com"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        d = {}
        for n, smokeddl in enumerate(soup.findAll("div", class_="smokeddl")[:-1], start=1):
            title = f"{n}. " + smokeddl.find(class_="smokettl").text
            d[title] = {}
            for smokeurl in smokeddl.findAll(class_="smokeurl"):
                res = smokeurl.strong.text
                links = {}
                for a in smokeurl.findAll("a"):
                    links[a.text] = a["href"]
                d[title][res] = links
        return d

    def search(self, query, page=1):
        raw = self.session.get(self.host + f"/page/{page}/", params={
            "s": query})
        soup = self.soup(raw)

        result = []
        for item in soup.findAll("div", class_="content"):
            d = {
                "title": item.h2.text,
                "id": self.getPath(item.a["href"])
            }
            for p in item.findAll("p"):
                if "genre" in p.text:
                    d["genre"] = [a.text for a in p.findAll(p)]
                elif "release" in p.text:
                    d["released"] = p.text.split("on ")[-1]
            result.append(d)
        return result
