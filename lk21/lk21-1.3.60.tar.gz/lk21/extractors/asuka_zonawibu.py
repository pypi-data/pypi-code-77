from . import BaseExtractor

class Asuka_Zonawibu(BaseExtractor):
    tag = "anime"
    host = "https://asuka.zonawibu.net"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        result = {}
        if (direct := soup.find("a", text="DIRECT DOWNLOAD")):
            result[a.text] = a["href"]

        for dl in soup.findAll("dl"):
            for smokeurl in dl.findAll(class_="smokeurl"):
                smokettl = smokeurl.findPrevious(class_="smokettl").text
                if not result.get(smokettl):
                    result[smokettl] = {}

                r = {}
                for a in smokeurl.findAll("a"):
                    r[a.text] = a["href"]
                result[smokettl][smokeurl.strong.text] = r
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}",
           params={"s": query})
        soup = self.soup(raw)

        result = []
        for postlist in soup.findAll(class_="postlist"):
            a = postlist.a
            r = {
                "id": self.getPath(a["href"]),
                "title": a.text
            }

            for y in postlist.findAll(class_=self.re.compile(r"auth(?:mobile)?")):
                if len(x := y.text.split(":")):
                    r[x[0]] = x[1]

            result.append(r)
        return result
