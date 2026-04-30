import json
import requests
from bs4 import BeautifulSoup


URL = "http://bdlaws.minlaw.gov.bd/act-print-367.html"


def scrape_constitution():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    # NOTE: selector may vary depending on site structure
    blocks = soup.find_all("div", class_="article")

    if not blocks:
        print("⚠️ No articles found. Site structure may have changed.")
        return []

    for block in blocks:
        try:
            article_tag = block.find("h3")
            title_tag = block.find("h4")
            text_tag = block.find("p")

            # safe extraction (avoid None crash)
            article = article_tag.get_text(strip=True) if article_tag else ""
            title = title_tag.get_text(strip=True) if title_tag else ""
            text = text_tag.get_text(strip=True) if text_tag else ""

            if not text:
                continue  # skip empty entries

            articles.append(
                {
                    "article": article,
                    "title": title,
                    "text": text,
                    "keywords": [],
                    "category": "Constitution",
                }
            )

        except Exception as e:
            print("Skipping block due to error:", e)
            continue

    return articles


def save_to_json(output_path="app/data/constitution-parse.json"):
    data = scrape_constitution()

    if not data:
        print("❌ No data scraped. Nothing to save.")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(data)} articles to {output_path}")


if __name__ == "__main__":
    save_to_json()
