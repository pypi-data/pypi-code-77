import re


def parse_range(raw):
    assert re.match(r"[\s\d:]+", raw), f"invalid syntax: {raw!r}"
    if "," in raw:
        for rg in re.split(r"\s*,\s*", raw):
            if ":" not in rg:
                yield rg
            else:
                assert len(re.findall(r":", raw)
                           ) <= 1, f"invalid syntax: {raw!r}"
                yield from parse_range(rg)
    else:
        spl = re.split(r"\s*:\s*", raw)
        if not spl[0]:
            spl[0] = "1"

        start, end = map(lambda x: int(x) if x else None, spl)
        if end:
            assert start < end, "angka pertama tidak boleh lebih dari angka kedua"
            yield from range(start, end + 1)
        else:
            while True:
                yield start
                start += 1
