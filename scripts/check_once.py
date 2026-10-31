#!/usr/bin/env python3
"""讀 urls.txt，抓頁面，試著找出價錢，跟上次比較。"""

from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

from notify_stub import notify

ROOT = Path(__file__).resolve().parents[1]
URLS_FILE = ROOT / "urls.txt"
DATA_FILE = ROOT / "data" / "last_prices.json"

PRICE_PATTERNS = [
    re.compile(r'"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?', re.I),
    re.compile(r'"priceAmount"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?', re.I),
    re.compile(r"(?:USD|SGD|HKD|US\$)\s*([0-9]+(?:\.[0-9]+)?)", re.I),
    re.compile(r"\$\s*([0-9]+(?:\.[0-9]+)?)"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def load_urls() -> list[str]:
    lines = URLS_FILE.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def load_last() -> dict:
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_last(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract_price(text: str) -> str | None:
    for pattern in PRICE_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1)
    return None


def check_url(client: httpx.Client, url: str) -> str:
    try:
        response = client.get(url, follow_redirects=True, timeout=30.0)
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        return f"ERROR: {exc}"
    price = extract_price(response.text)
    return price if price else "UNKNOWN"


def main() -> None:
    urls = load_urls()
    last = load_last()
    current: dict[str, str] = {}

    with httpx.Client(headers=HEADERS) as client:
        for url in urls:
            price = check_url(client, url)
            current[url] = price
            previous = last.get(url)
            print(f"{url}\n  now={price}  before={previous}")
            if previous is not None and previous != price and price != "UNKNOWN":
                notify(f"PRICE CHANGED\n{url}\n{previous} -> {price}")

    save_last(current)
    print("Saved", DATA_FILE)


if __name__ == "__main__":
    main()
