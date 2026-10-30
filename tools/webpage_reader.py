import requests
from bs4 import BeautifulSoup

def read_page(url):

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for tag in soup(
        ["script", "style", "nav", "footer"]
    ):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text[:4000]