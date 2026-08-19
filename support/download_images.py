"""Download street images with stop signs from the internet.

Usage:
    python scripts/download_images.py
"""

from icrawler.builtin import BingImageCrawler

KEYWORDS = [
    "stop sign street view",
    "intersection stop sign",
    "urban stop sign road",
    "stop sign on road",
    "stop sign traffic intersection",
]

SAVE_DIR = "raw"

crawler = BingImageCrawler(
    storage={"root_dir": SAVE_DIR},
    log_level=40,
)

for keyword in KEYWORDS:
    print(f"Downloading images for: {keyword}")
    crawler.crawl(keyword=keyword, max_num=20)
    print("Done.\n")

print("Download finished. Review files in the 'raw' folder and")
print("pick the best 50 images that clearly show stop signs.")
print("Move them to dataset/images/ and rename them stop_001.jpg .. stop_050.jpg")
