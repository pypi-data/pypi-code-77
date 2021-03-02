from . import BaseExtractor


class Nekonime(BaseExtractor):
    host = "https://nekonime.stream"
    tag = "anime"

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

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

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
