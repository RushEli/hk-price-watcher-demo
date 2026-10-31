# hk-price-watcher-demo

香港跨境價差監控示範（小學生也能跟）。

## 這個專案在做什麼？

盯兩個商品網頁的價錢。價錢變了，就在終端機印出 `PRICE CHANGED`。

示範商品：Anker USB-C 線（型號 A82E2）

- Amazon US：https://www.amazon.com/Anker-Flexible-Multi-Color-Braided-Charging/dp/B0CZ42N46L
- Anker Singapore：https://anker.com.sg/products/anker-usb-c-to-usb-c-cable-3ft-6ft-240w-upcycled-braided-fast-charging-type-c-for-iphone-16-macbook-pro-a82e2

## 最快怎麼跑？

1. 安裝 Python 3
2. 在專案資料夾執行：

```bash
pip install -r requirements.txt
python scripts/check_once.py
```

3. 再跑一次。如果價錢跟上次不一樣，會看到 `PRICE CHANGED`。

## 檔案說明

- `urls.txt`：要盯的網址
- `scripts/check_once.py`：抓頁面、找價錢、跟上次比較
- `data/last_prices.json`：上次看到的價錢（第一次跑會自動建立）
- `.env.example`：之後接 Telegram／email 用
