from . import BaseExtractor


class Samehadaku(BaseExtractor):
    tag = "anime"
    host = "https://samehadaku.vip"

    def extract(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dan metadata dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'

        Returns:
              dict: hasil 'scrape' halaman web
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if id.startswith("anime/"):
            ch = {}
            if (listeps := soup.findAll(class_="epsleft")):
                for li in listeps:
                    a = li.find("a")
                    ch[a.text] = self.getPath(a["href"])
            if (batch := soup.find(class_="listbatch")):
                ch[batch.text] = self.getPath(batch.a["href"])
            return ch

        result = {}
        for dl in soup.findAll(class_="download-eps"):
            d = {}
            for li in dl.findAll("li"):
                item = {}
                for a in li.findAll("a"):
                    item[a.text] = a["href"]
                d[li.strong.text] = item
            result[dl.p.text] = d
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        res = []
        for article in soup.findAll("article", class_="animpost"):
            result = {
                "id": self.getPath(article.find("a")["href"])
            }

            for k in ("score", "title", "type", "genres"):
                if (v := article.find(class_=k)):
                    name = " ".join(v["class"])
                    if (aa := v.findAll("a")):
                        result[name] = [a.text for a in aa]
                    elif v.text:
                        result[name] = v.text
            res.append(result)
        return res
