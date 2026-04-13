import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
            }
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return ""
        
        return res.text
    except:
         print("Request failed:",url)
         return ""
    

def extract_emails(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(pattern, text)))

def get_pages(html, base_url):
    soup = BeautifulSoup(html ,"html.parser")
    links = []

    keywords = ["contact", "about", "support", "help"]

    for link in soup.find_all("a", href=True):
        href = link["href"].lower()

        if any (k in href for k in keywords):
            full_url = urljoin(base_url, link["href"])
            links.append(full_url)
        
    return list(set(links))

def process_website(website):
    if not website:
        return []

    if "justdial" in website.lower():
        return []
    
    html = get_html(website)

    if not html:
        return []
    
    emails = extract_emails(html)

    pages = get_pages(html,website)
    for page in pages[:3]:
        page_html = get_html(page)
        emails += extract_emails(page_html)

    return list(set(emails))