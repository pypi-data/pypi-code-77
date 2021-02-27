import requests

API = "https://api.exchangeratesapi.io"


def _load_rates(date="latest", base="EUR") -> dict:
    _base = base if isinstance(base, str) else base.name
    _url = f"{API}/{date}?base={_base}"
    response = requests.get(_url)
    return response.json()


def _load_history(start_at, end_at, base="EUR") -> dict:
    _base = base if isinstance(base, str) else base.name
    _url = f"{API}/history?start_at={start_at}&end_at={end_at}&base={_base}"
    response = requests.get(_url)
    return response.json()
