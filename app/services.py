import requests
from bs4 import BeautifulSoup
from readability import Document
from langdetect import detect, DetectorFactory
import re

DetectorFactory.seed = 0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (MetadataArticleBot/1.0)"
}

def fetch_url(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


# ======================
# METADATA EXTRACTOR
# ======================
def extract_metadata(url: str) -> dict:
    html = fetch_url(url)
    soup = BeautifulSoup(html, "html.parser")

    def get_meta(name=None, prop=None):
        if name:
            tag = soup.find("meta", attrs={"name": name})
        else:
            tag = soup.find("meta", attrs={"property": prop})
        return tag["content"] if tag and tag.get("content") else None

    title = soup.title.string.strip() if soup.title else None
    description = get_meta(name="description") or get_meta(prop="og:description")
    image = get_meta(prop="og:image")
    site_name = get_meta(prop="og:site_name")

    return {
        "url": url,
        "title": title,
        "description": description,
        "image": image,
        "site_name": site_name,
    }


# ======================
# SIMPLE SUMMARY MAKER
# ======================
def make_summary(text: str, max_sentences: int = 3) -> str:
    if not text:
        return ""

    sentences = re.split(r'(?<=[.!?])\s+', text)

    summary_sentences = sentences[:max_sentences]
    summary = " ".join(summary_sentences)

    return summary.strip()


# ======================
# ARTICLE EXTRACTOR
# ======================
def extract_article(url: str) -> dict:
    html = fetch_url(url)

    doc = Document(html)
    content_html = doc.summary(html_partial=True)
    soup = BeautifulSoup(content_html, "html.parser")

    text = soup.get_text(separator="\n", strip=True)

    word_count = len(text.split())

    summary = make_summary(text, max_sentences=3)

    return {
        "url": url,
        "title": doc.short_title(),
        "word_count": word_count,
        "summary": summary,          
        "content_text": text,
        "content_html": content_html,
    }
