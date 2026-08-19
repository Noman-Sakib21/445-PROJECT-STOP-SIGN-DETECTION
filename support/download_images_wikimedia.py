"""Download street stop-sign images from Wikimedia Commons.

Reliable fallback when icrawler/Bing is blocked (403).
Downloads to raw/ and deduplicates by file hash.

Usage:
    python scripts/download_images_wikimedia.py
"""

import hashlib
import pathlib
import sys
import time

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API = "https://commons.wikimedia.org/w/api.php"
SAVE_DIR = "raw"
TARGET = 60
OUT_WIDTH = 1024

QUERIES = [
    "stop sign street",
    "stop sign intersection",
    "stop sign road traffic",
    "stop sign urban",
    "octagonal stop sign road",
]

session = requests.Session()
session.headers.update({"User-Agent": "StopSignDL/1.0 (student ML project; contact: local)"})

PATH = pathlib.Path(__file__).resolve().parent.parent / SAVE_DIR
PATH.mkdir(parents=True, exist_ok=True)
SEEN = set()


def search_files(query, limit=30):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": "filetype:bitmap " + query,
        "gsrnamespace": "6",
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "iiurlwidth": OUT_WIDTH,
        "format": "json",
    }
    r = session.get(API, params=params, timeout=30)
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        info = page.get("imageinfo", [{}])[0]
        mime = info.get("mime", "")
        if mime not in ("image/jpeg", "image/png"):
            continue
        width = info.get("width", 0)
        if width < 400:
            continue
        thumb = info.get("thumburl") or info.get("url")
        if thumb:
            yield page.get("title", ""), thumb


def download(url, retries=6):
    for attempt in range(retries):
        r = session.get(url, timeout=30)
        if r.status_code == 429:
            wait = 5 * (attempt + 1)
            print(f"  ...rate-limited, waiting {wait}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.content
    raise RuntimeError("too many 429 responses")


def main():
    total = 0
    for query in QUERIES:
        if total >= TARGET:
            break
        print(f"Query: {query}")
        for title, url in search_files(query):
            if total >= TARGET:
                break
            try:
                content = download(url)
            except Exception as e:
                print(f"  skip {title}: {e}")
                continue

            digest = hashlib.md5(content).hexdigest()
            if digest in SEEN:
                continue
            SEEN.add(digest)

            ext = ".jpg" if content[:3] == b"\xff\xd8\xff" else ".png"
            name = f"stop_{total + 1:03d}{ext}"
            (PATH / name).write_bytes(content)
            print(f"  saved {name}  <{len(content) // 1024} KB>")
            total += 1
            time.sleep(1.2)
        time.sleep(2.0)

    print(f"\nTotal downloaded: {total} images -> {SAVE_DIR}/")


if __name__ == "__main__":
    main()