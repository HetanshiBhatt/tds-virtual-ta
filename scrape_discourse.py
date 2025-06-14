from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

# Set your actual _forum_session cookie here
forum_session_cookie = "REPLACE_THIS_WITH_YOUR_COOKIE"

# Set up Selenium Chrome driver
options = Options()
options.add_argument("--start-maximized")

service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Open the Discourse forum (not JSON endpoint)
url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
driver.get(url)
time.sleep(3)  # Wait for initial page load

# Inject the forum_session cookie to simulate login
driver.add_cookie({
    "name": "_forum_session",
    "value": forum_session_cookie,
    "domain": "discourse.onlinedegree.iitm.ac.in",
    "path": "/"
})

# Refresh to apply cookie and view logged-in content
driver.refresh()
time.sleep(5)  # Wait for dynamic content to load

# Debug: Print all <a> tags (first 20 only)
a_tags = driver.find_elements(By.TAG_NAME, "a")
print(f"🔎 Found {len(a_tags)} <a> tags")
for a in a_tags[:20]:
    print("→", a.text.strip(), "|", a.get_attribute("href"))

# Try to find post titles (discourse style)
posts = []
title_links = driver.find_elements(By.CSS_SELECTOR, "a.title")

for link in title_links:
    title = link.text.strip()
    href = link.get_attribute("href")
    if title and href:
        posts.append({
            "title": title,
            "url": href
        })

# Save to JSON
with open("discourse_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2)

print(f"✅ Saved {len(posts)} posts to 'discourse_posts.json'")

# Cleanup
driver.quit()
