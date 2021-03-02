from . import BaseExtractor


class Anibatch(BaseExtractor):
    tag = "anime"
    host = "https://o.anibatch.me/"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:h
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        if (content := self.last_soup.find(class_="entry-content")):
            def setItem(id, key=None):
                if (value := self.re.search(r"(?i){}\s*:\s*([^>]+?) *?\n".format(id), content.text)):
                    value = self.re.split(r"\s*,\s*", value.group(1))
                    if len(value) == 1:
                        value = value[0]
                    meta[key or self.re.sub(r" ", "_", id)] = value

            setItem("judul anime", "judul")
            setItem("judul alternatif")
            setItem("tipe anime", "tipe")
            setItem("status anime", "status")
            setItem("jumlah episode")
            setItem("musim rilis", "musim")
            setItem("studio yang memproduksi", "studio")
            setItem("genre")
            setItem("durasi per episode", "durasi")
            setItem("Skor di MyAnimeList", "score")

        if (h2 := soup.find("h2", text=self.re.compile(r"Sinopsis[^>]+"))):
            desc = []
            for p in h2.findAllNext("p"):
                if p.center:
                    break
                desc.append(p.text)
            meta["sinopsis"] = " ".join(desc)
        elif (ogDesc := soup.find(r"meta", property="og:description")):
            content = self.re.sub(r"\[[^]]+?]\s*$", "[^>]+", ogDesc["content"])
            if (fullDesc := soup.find(text=self.re.compile(content))):
                meta["sinopsis"] = fullDesc

        if (h2 := soup.find("h2", text="Main Character")):
            meta["karakter"] = [
                figure.text for figure in h2.findAllNext("figure")]

        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        dlx = soup.find(class_="dlx")
        result = {}

        for table in dlx.findAll("table"):
            if not table.strong:
                continue

            if (h4 := table.findPrevious("h4", style="text-align: center")):
                eps = h4.text
            elif (prevTable := table.findPrevious("table")):
                eps = prevTable.text

            d = {}
            res = None
            for tr in table.findAll("tr"):
                if not tr.a:
                    res = tr.text
                    d[res] = {}
                    continue
                for a in tr.findAll("a"):
                    d[res][a.text] = a["href"]
            result[eps] = d
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

        result = []
        for artikel in soup.findAll("article"):
            a = artikel.find("a")
            if not a.img:
                continue
            result.append({
                "title": a["title"],
                "id": self.getPath(a["href"])
            })
        return result
