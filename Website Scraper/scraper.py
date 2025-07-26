import requests
from bs4 import BeautifulSoup
import json
from rapidfuzz import fuzz

# ------------------------ USER INPUT SECTION ------------------------
# ✅ Set the page URL you want to scrape (without ?page=)
WEBSITE_URL = "https://www.kpopalbums.com/collections/lastest-release"

# ✅ Set the part of the URL that identifies product pages
PRODUCT_URL_PATTERN = "https://www.kpopalbums.com/collections/lastest-release/products/"

# ✅ Set the similarity threshold (0–100)
SIMILARITY_THRESHOLD = 70

# ✅ Set max pages to scan (use a safe number like 30)
MAX_PAGES = 30
# --------------------------------------------------------------------

def extract_product_urls(base_url, pattern, max_pages=20):
    """Extract product URLs from multiple paginated pages."""
    print(f"Scraping multiple pages starting from {base_url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    product_links = set()
    base_domain = f"https://{base_url.split('/')[2]}"

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"🔎 Fetching page {page}...")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"⚠️ Skipping page {page} (status code {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        product_blocks = soup.find_all("a", href=True)

        page_links = 0
        for link in product_blocks:
            href = link['href']
            full_url = href if href.startswith("http") else f"{base_domain}{href}"
            if full_url.startswith(pattern):
                if full_url not in product_links:
                    product_links.add(full_url)
                    page_links += 1

        if page_links == 0:
            print("🚫 No more product links found. Stopping.")
            break

    print(f"✅ Total unique product URLs found: {len(product_links)}")
    return list(product_links)


def are_similar(url1, url2, threshold):
    """Check if two product URLs are similar based on fuzzy match."""
    base1 = url1.split("/products/")[-1].split("?")[0].lower()
    base2 = url2.split("/products/")[-1].split("?")[0].lower()
    score = fuzz.ratio(base1, base2)
    return score >= threshold


def group_similar_products(product_urls, threshold):
    """Group similar product URLs ensuring no URL appears in more than one group."""
    grouped = []
    unused_urls = set(product_urls)

    while unused_urls:
        current = unused_urls.pop()
        group = [current]

        similar_urls = set()
        for other in unused_urls:
            if are_similar(current, other, threshold):
                group.append(other)
                similar_urls.add(other)

        unused_urls -= similar_urls
        grouped.append({"urls": group})

    print(f"✅ Grouped into {len(grouped)} sets of similar products.")
    return grouped


def main():
    product_urls = extract_product_urls(WEBSITE_URL, PRODUCT_URL_PATTERN, max_pages=MAX_PAGES)
    grouped_urls = group_similar_products(product_urls, SIMILARITY_THRESHOLD)

    with open("output.json", "w") as f:
        json.dump(grouped_urls, f, indent=2)

    print("✅ Done! Grouped results saved to output.json")


if __name__ == "__main__":
    main()
