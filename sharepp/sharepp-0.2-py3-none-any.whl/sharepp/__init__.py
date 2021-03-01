from bs4 import BeautifulSoup
import requests
import sys

onvista_url = "https://www.onvista.de/"


def parse_price(isin):
    response = requests.get(onvista_url + isin)
    parsed_html = BeautifulSoup(response.text, "html.parser")
    try:
        # Single share.
        price_span = parsed_html.find("ul", class_="KURSDATEN").find("span")
        price_string = price_span.text
    except AttributeError:
        # ETF.
        column_div = parsed_html.find("div", class_="col col--sm-4 col--md-4 col--lg-4 col--xl-4")
        price_span = column_div.find("data", class_="text-nowrap")
        price_string = price_span.text.split(" ")[0]

    price_string = price_string.replace('.', '').replace(',', '.')

    return float(price_string)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You must provide exactly one argument.")
    else:
        print(parse_price(sys.argv[1]))
