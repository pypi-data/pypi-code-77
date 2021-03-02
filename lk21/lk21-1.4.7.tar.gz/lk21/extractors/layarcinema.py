from . import BaseExtractor


class Layarcinema():
    tag = None
    host = "http://213.166.69.166"

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

        self._write(soup)

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

        raw = self.session.get(f"{self.host}/page/{page}",
                               params={"s": query})
        soup = self.soup(raw)

        result = []
        for item in soup.findAll(class_="ml-item"):
            a = item.find("a")
            r = {
                "id": self.getPath(a["href"]),
                "title": a["title"]
            }

            for k in ("mli-quality", "mli-rating", "mli-durasi"):
                if (i := item.find(class_=k)) and i.text:
                    r[k] = i.text
            result.append(r)
        return result
