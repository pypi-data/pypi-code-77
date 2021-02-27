from . import BaseExtractor


class Anikyojin(BaseExtractor):
    host = "https://anikyojin.net"
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

        result = {}
        for dc in soup.findAll(class_="downloadcloud"):
            reso = {}
            for li in dc.findAll("li"):
                d = {}
                for a in li.findAll("a"):
                    d[a.text] = a["href"]
                reso[li.strong.text] = d
            result[dc.h2.text] = reso
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
            "s": query, "post_type": "post"})
        soup = self.soup(raw)

        r = []
        for article in soup.findAll(class_="artikel"):
            a = article.h2.find("a")

            result = {
                "title": a.text,
                "id": self.getPath(a["href"])
            }

            for li in article.find(class_="info").findAll("li"):
                k, v = self.re.split(r"\s*:\s*", li.text)
                if "," in v:
                    v = self.re.split(r"\s*,\s*", v)
                result[k] = v

            r.append(result)
        return r
