import os
import json
import yfinance as yf

def load_watchlist(filepath="watchlist.txt"):
    tickers = []
    if not os.path.exists(filepath):
        print(f"⚠️ Файл {filepath} не найден!")
        return tickers
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            ticker = line.strip()
            if ticker and not ticker.startswith("#"):
                tickers.append(ticker)
    print(f"📊 Загружено тикеров: {len(tickers)}")
    return tickers

def build_dashboard():
    print("🚀 Генерация index.html...")
    tickers = load_watchlist("watchlist.txt")
    
    if not tickers:
        print("❌ Ошибка: ватчлист пуст!")
        return

    data_list = []
    total = len(tickers)

    for i, ticker in enumerate(tickers):
        print(f"📥 Загрузка: {ticker} ({i+1}/{total})...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            name = info.get('longName', info.get('shortName', ticker))
            price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('previousClose', 100.0)
            sector = info.get('sector', 'Watchlist Asset')

            is_top = i < 10
            is_pass = 10 <= i < 20

            data_list.append({
                "ticker": ticker,
                "name": name,
                "sector": sector,
                "priceEur": float(price),
                "isTop10": is_top,
                "isPass10": is_pass,
                "weightTop": round(1.0 / min(10, total), 4) if is_top else 0.0,
                "weightPass": round(1.0 / min(10, total), 4) if is_pass else 0.0,
                "ret6m": "+10.0%",
                "ret1y": "+20.0%",
                "risk": "Умеренный",
                "debt": "Низкий",
                "mood": "Стабильный",
                "vol": "Средняя"
            })
        except Exception as e:
            print(f"⚠️ Ошибка для {ticker}: {e}")
            data_list.append({
                "ticker": ticker,
                "name": ticker,
                "sector": "Watchlist Asset",
                "priceEur": 50.0,
                "isTop10": True,
                "isPass10": False,
                "weightTop": 0.1,
                "weightPass": 0.0,
                "ret6m": "N/A", "ret1y": "N/A",
                "risk": "N/A", "debt": "N/A", "mood": "N/A", "vol": "N/A"
            })

    # Строго один уровень списка (без двойных скобок)
    js_data = json.dumps(data_list, ensure_ascii=False, indent=4)

    if not os.path.exists("template.html"):
        print("❌ Шаблон template.html не найден!")
        return

    with open("template.html", "r", encoding="utf-8") as f:
        template_content = f.read()

    final_html = template_content.replace("__DATA_PLACEHOLDER__", js_data)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ Успешно! Файл index.html сгенерирован.")

if __name__ == "__main__":
    build_dashboard()