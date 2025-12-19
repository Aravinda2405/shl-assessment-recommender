import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_assessment_links():
    response = requests.get(CATALOG_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/assessments/" in href and "job" not in href:
            links.add(BASE_URL + href)

    return list(links)


def scrape_assessment(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find("h1")
    name = name.get_text(strip=True) if name else ""

    description = soup.get_text(" ", strip=True)[:1500]

    text = description.lower()
    test_type = []
    if "personality" in text or "behavior" in text:
        test_type.append("P")
    if "knowledge" in text or "skill" in text or "ability" in text:
        test_type.append("K")

    return {
        "name": name,
        "url": url,
        "description": description,
        "duration": "",
        "adaptive_support": "",
        "remote_support": "",
        "test_type": test_type
    }


def main():
    print("Fetching assessment links...")
    links = get_assessment_links()
    print(f"Found {len(links)} assessment links")

    results = []

    for i, link in enumerate(links):
        print(f"Scraping {i + 1}/{len(links)}")
        try:
            data = scrape_assessment(link)
            if data["name"]:
                results.append(data)
            time.sleep(1)
        except Exception as e:
            print("Error:", e)

    with open("data/raw/shl_catalog_raw.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Scraping completed successfully")


if __name__ == "__main__":
    main()
