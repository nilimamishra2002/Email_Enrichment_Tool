import requests
from bs4 import BeautifulSoup


def scrape_website(domain):
    """
    Scrapes multiple pages from a domain to gather text
    useful for sector classification.
    """

    urls = [
        f"https://{domain}",
        f"https://www.{domain}",
        f"https://{domain}/about",
        f"https://{domain}/about-us",
        f"https://{domain}/company",
        f"https://{domain}/services"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    collected_text = []

    for url in urls:

        try:
            response = requests.get(url, headers=headers, timeout=3)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            text_parts = []

            # Title
            if soup.title and soup.title.string:
                text_parts.append(soup.title.string)

            # Meta description
            meta = soup.find("meta", attrs={"name": "description"})
            if meta and meta.get("content"):
                text_parts.append(meta["content"])

            # OpenGraph description
            og = soup.find("meta", attrs={"property": "og:description"})
            if og and og.get("content"):
                text_parts.append(og["content"])

            # Headings
            headings = soup.find_all(["h1", "h2", "h3"])
            for h in headings[:15]:
                text_parts.append(h.get_text())

            # Paragraphs
            paragraphs = soup.find_all("p")
            for p in paragraphs[:25]:
                text_parts.append(p.get_text())

            page_text = " ".join(text_parts)

            if page_text:
                collected_text.append(page_text)

        except Exception:
            continue

    return " ".join(collected_text)