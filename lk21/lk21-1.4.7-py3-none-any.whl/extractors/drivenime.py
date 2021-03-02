from . import BaseExtractor


class Drivenime(BaseExtractor):
    tag = "anime"
    host = "https://drivenime.com"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'

        {
          "judul": "",
          "judul_alternatif": "",
          "tipe": "",
          "status": "",
          "jumlah_episode": "",
          "tayang": "",
          "musim": "",
          "studio": "",
          "genre": "",
          "durasi": "",
          "MAL": 0.1,
          "rating": "",
          "karakter": ""
        }

        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        self._write(soup)

        meta = self.MetaSet()
        return meta

    def extract(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'

        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        dl = soup.find(class_="post-single-content")
        for p in dl.findAll("p"):
            if (p.find("a")) and "download" in p.text.lower():
                break
        title = self.re.findall(r"(?s)a>\s*(\[[^>]+?\])\s*<", str(p))
        return {
            ttl: a["href"] for ttl, a in zip(title, p.findAll("a"))
        }

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        result = []
        for post in soup.findAll(class_="post"):
            a = post.find("a")
            r = {
                "title": a["title"],
                "id": self.getPath(a["href"])
            }

            if (genre := post.find(class_="theauthor")):
                r["genre"] = [a.text for a in genre.findAll("a")]

            result.append(r)
        return result
