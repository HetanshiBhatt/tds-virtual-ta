from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

DISCUSSION_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to running Chrome

driver = webdriver.Chrome(options=options)

# Navigate to the page
driver.get(DISCUSSION_URL)
time.sleep(5)

# Scroll to load content
SCROLL_PAUSE = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get topic links
topics = driver.find_elements(By.CSS_SELECTOR, "a.title")
topic_links = list(set([t.get_attribute("href") for t in topics if "/t/" in t.get_attribute("href")]))
print(f"🔗 Found {len(topic_links)} topic links")

# Scrape content
data = []
for link in topic_links:
    driver.get(link)
    time.sleep(3)
    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1").text
        posts = driver.find_elements(By.CSS_SELECTOR, ".cooked")
        content = "\n\n".join([p.text for p in posts])
        data.append({"title": title, "content": content})
    except Exception as e:
        print(f"❌ Error on {link}: {e}")

with open("discourse_posts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

driver.quit()
print(f"✅ Scraped {len(data)} posts into discourse_posts.json")
