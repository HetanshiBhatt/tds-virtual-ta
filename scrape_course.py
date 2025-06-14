import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://tds.s-anand.net"
COURSE_PATH = "/#/2025-01/"
MODULE_PREFIX = "2025-01/"  # used to build proper URLs

# Load the main page
main_url = f"{BASE_URL}/{COURSE_PATH}"
response = requests.get(main_url)

if response.status_code != 200:
    print(f"❌ Failed to fetch course homepage — Status code: {response.status_code}")
    exit()

# Parse the HTML and extract all sidebar links
soup = BeautifulSoup(response.text, "html.parser")

# fallback in case JS is needed — we'll use hardcoded list instead
print("❌ This site uses client-side JavaScript — static scraping won't work from this URL directly.")
print("🔁 Switching to known list of TDS modules (hardcoded) for Jan 2025 batch...")

# ✅ Use known URLs (manually gathered or viewed from browser developer tools)
module_slugs = [
    "intro", "eda", "visualisation", "eda2", "eda3",
    "eda4", "eda5", "eda6", "eda7", "eda8", "eda9",
    "eda10", "regression", "ml", "ml2", "ml3",
    "ml4", "ml5", "ml6", "ml7"
]

data = []

for slug in module_slugs:
    url = f"{BASE_URL}/{MODULE_PREFIX}{slug}.html"
    print(f"🔎 Fetching: {url}")
    page = requests.get(url)
    
    if page.status_code != 200:
        print(f"⚠️ Failed to fetch {slug} — status {page.status_code}")
        continue

    soup = BeautifulSoup(page.text, "html.parser")
    text = soup.get_text(separator="\n").strip()

    data.append({
        "title": slug,
        "url": url,
        "content": text
    })

    time.sleep(0.5)  # avoid hammering the server

# Save all modules to a JSON file
with open("course_content.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Scraped {len(data)} modules into course_content.json")
