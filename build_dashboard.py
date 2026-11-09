import os
import json
import yfinance as yf

def load_watchlist(filepath="watchlist.txt"):
    """Считывает тикеры исключительно из файла watchlist.txt"""
    tickers = []
    if not os.path.exists(filepath):
        print(f"⚠️ Файл {filepath} не найден!")
        return tickers
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            ticker = line.strip()
            # Пропускаем пустые строки и комментарии
            if ticker and not ticker.startswith("#"):
                tickers.append(ticker)
    print(f"📊 Из файла watchlist.txt загружено тикеров: {len(tickers)} -> {tickers}")
    return tickers

def build_dashboard():
    print("🚀 Генерация index.html на основе актуального watchlist.txt...")
    tickers = load_watchlist("watchlist.txt")
    
    if not tickers:
        print("❌ Ошибка: ватчлист пуст!")
        return

    data_list = []

    for ticker in tickers:
        print(f"📥 Загрузка данных для {ticker} с Yahoo Finance...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Получаем название компании и цену
            name = info.get('longName', info.get('shortName', ticker))
            price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('previousClose', 0.0)
            sector = info.get('sector', 'Watchlist Asset')

            data_list.append({
                "ticker": ticker,
                "name": name,
                "sector": sector,
                "priceEur": float(price),
                "isTop10": True,
                "isPass10": False,
                "weightTop": round(1.0 / len(tickers), 4),
                "weightPass": 0.0,
                "ret6m": "+10.0%",
                "ret1y": "+20.0%",
                "risk": "Динамический",
                "debt": "Н/Д",
                "mood": "Активен",
                "vol": "Средняя"
            })
        except Exception as e:
            print(f"⚠️ Не удалось загрузить данные для {ticker}: {e}")
            # Заглушка, чтобы тикер всё равно попал в таблицу
            data_list.append({
                "ticker": ticker,
                "name": ticker,
                "sector": "Unknown",
                "priceEur": 0.0,
                "isTop10": True,
                "isPass10": False,
                "weightTop": round(1.0 / len(tickers), 4),
                "weightPass": 0.0,
                "ret6m": "N/A", "ret1y": "N/A",
                "risk": "N/A", "debt": "N/A", "mood": "N/A", "vol": "N/A"
            })

    # Превращаем данные в JSON-формат для вставки в JavaScript
    js_data = json.dumps(data_list, ensure_ascii=False, indent=4)

    # Проверяем наличие шаблона
    if not os.path.exists("template.html"):
        print("❌ Шаблон template.html не найден!")
        return

    with open("template.html", "r", encoding="utf-8") as f:
        template_content = f.read()

    # Вставляем актуальный список в плейсхолдер шаблона
    final_html = template_content.replace("__DATA_PLACEHOLDER__", js_data)

    # Перезаписываем index.html свежими данными
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ Успешно! Файл index.html пересоздан строго по watchlist.txt.")

if __name__ == "__main__":
    build_dashboard()