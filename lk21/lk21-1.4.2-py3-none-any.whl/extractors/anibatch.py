from . import BaseExtractor


class Anibatch(BaseExtractor):
    tag = "anime"
    host = "https://o.anibatch.me/"

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

        dlx = soup.find(class_="dlx")
        result = {}
        for table in dlx.findAll("table"):
            d = {}
            for a in table.findAll("a"):
                d[a.text] = a["href"]
            strong = table.find("strong").text
            result[strong] = d
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
                    dengan struktur;

                    [
                      {
                        'id':  type 'str',
                        'title': type 'str'
                      }
                    ]
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        result = []
        for artikel in soup.findAll("article"):
            a = artikel.find("a")
            result.append({
                "title": a["title"],
                "id": self.getPath(a["href"])
            })
        return result
