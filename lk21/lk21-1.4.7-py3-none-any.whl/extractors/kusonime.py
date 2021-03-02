from . import BaseExtractor


class Kusonime(BaseExtractor):
    tag = "anime"
    host = "https://kusonime.com"

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

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

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
