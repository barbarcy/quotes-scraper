#!/usr/bin/env python3
"""
Simple scraper for http://quotes.toscrape.com
Saves output to a CSV with columns: text, author, tags
Usage:
    python scraper.py --output quotes.csv --delay 1.0 --user-agent "portfolio-scraper/1.0 (+mailto:you@example.com)"
"""
import argparse
import csv
import time
import sys
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

BASE = "http://quotes.toscrape.com"


def scrape_page(session: requests.Session, url: str) -> List[Dict[str, str]]:
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    quotes = []
    for q in soup.select(".quote"):
        text_el = q.select_one(".text")
        author_el = q.select_one(".author")
        tags_el = q.select(".tags .tag")
        text = text_el.get_text(strip=True) if text_el else ""
        author = author_el.get_text(strip=True) if author_el else ""
        tags = [t.get_text(strip=True) for t in tags_el] if tags_el else []
        quotes.append({"text": text, "author": author, "tags": ",".join(tags)})
    return quotes


def find_next(session: requests.Session, url: str) -> str:
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    next_btn = soup.select_one(".pager .next a")
    if next_btn:
        return next_btn.get("href")
    return ""


def paginate_and_scrape(session: requests.Session, base: str, delay: float = 1.0) -> List[Dict[str, str]]:
    page = "/"
    all_quotes = []
    seen_urls = set()
    while page:
        url = base.rstrip("/") + page
        if url in seen_urls:
            print("Detected loop; stopping.", file=sys.stderr)
            break
        seen_urls.add(url)
        print("Scraping", url)
        quotes = scrape_page(session, url)
        all_quotes.extend(quotes)
        next_href = find_next(session, url)
        if next_href:
            page = next_href
            time.sleep(delay)
        else:
            page = ""
    return all_quotes


def save_csv(rows: List[Dict[str, str]], filename: str = "quotes.csv"):
    if not rows:
        print("No rows to save.", file=sys.stderr)
        return
    fieldnames = ["text", "author", "tags"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args():
    p = argparse.ArgumentParser(description="Scrape quotes.toscrape.com and save to CSV")
    p.add_argument("--base", default=BASE, help="Base URL to scrape")
    p.add_argument("--output", default="quotes.csv", help="Output CSV filename")
    p.add_argument("--delay", type=float, default=1.0, help="Delay between page requests (s)")
    p.add_argument(
        "--user-agent",
        default="portfolio-scraper/1.0 (+mailto:your-email@example.com)",
        help="User-Agent header to use",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})
    try:
        rows = paginate_and_scrape(session, args.base, delay=args.delay)
        save_csv(rows, args.output)
        print(f"Saved {len(rows)} quotes to {args.output}")
    except requests.HTTPError as e:
        print("HTTP error:", e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
        sys.exit(1)