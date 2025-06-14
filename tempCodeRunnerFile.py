import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Configure Chrome to run in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

# Start the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34/l/latest"
print(f"🔄 Opening page: {url}")
driver.get(url)

# Wait for JavaScript to render the posts
time.sleep(5)

# Extract posts
posts = []
base_url = "https://discourse.onlinedegree.iitm.ac.in"

# Debug: Print all <a> tags
a_tags = driver.find_elements(By.TAG_NAME, "a")
print(f"🔎 Found {len(a_tags)} <a> tags")
for a in a_tags[:20]:  # print only first 20
    print("→", a.text.strip(), "|", a.get_attribute("href"))


for el in elements:
    title = el.text.strip()
    href = el.get_attribute("href")
    if title and href:
        posts.append({"title": title, "url": href})

# Save to JSON
with open("discourse_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2)

print(f"✅ Saved {len(posts)} posts to 'discourse_posts.json'")
driver.quit()
