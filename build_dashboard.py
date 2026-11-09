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
    return tickers

def build_dashboard():
    print("🚀 Генерация дашборда на основе watchlist.txt...")
    tickers = load_watchlist("watchlist.txt")
    
    if not tickers:
        print("❌ Ватчлист пуст!")
        return

    data_list = []

    for ticker in tickers:
        print(f"📥 Загрузка данных для {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Получаем имя и цену (с запасными вариантами, если поле отсутствует)
            name = info.get('longName', info.get('shortName', ticker))
            
            # Пробуем взять текущую цену из разных полей yfinance
            price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('previousClose', 0.0)
            
            # Определяем примерный сектор или ставим дефолтный
            sector = info.get('sector', 'Watchlist Asset')

            data_list.append({
                "ticker": ticker,
                "name": name,
                "sector": sector,
                "priceEur": float(price),
                "isTop10": True,      # По умолчанию выводим во вкладку роста
                "isPass10": False,
                "weightTop": 1.0 / len(tickers), # Равномерный вес для динамики
                "weightPass": 0.0,
                "ret6m": "+10.0%",     # Можно заменить на реальный расчет при желании
                "ret1y": "+20.0%",
                "risk": "Динамический",
                "debt": "Н/Д",
                "mood": "Активен",
                "vol": "Средняя"
            })
        except Exception as e:
            print(f"⚠️ Ошибка загрузки {ticker}: {e}")
            # Добавляем заглушку, чтобы тикер все равно отобразился в таблице
            data_list.append({
                "ticker": ticker,
                "name": ticker,
                "sector": "Unknown",
                "priceEur": 0.0,
                "isTop10": True,
                "isPass10": False,
                "weightTop": 1.0 / len(tickers),
                "weightPass": 0.0,
                "ret6m": "N/A", "ret1y": "N/A",
                "risk": "N/A", "debt": "N/A", "mood": "N/A", "vol": "N/A"
            })

    # Превращаем список Python в формат JavaScript-массива
    js_data = json.dumps(data_list, ensure_ascii=False, indent=4)

    # Читаем шаблон template.html
    if not os.path.exists("template.html"):
        print("❌ Шаблон template.html не найден!")
        return

    with open("template.html", "r", encoding="utf-8") as f:
        template_content = f.read()

    # Заменяем плейсхолдер на реальные данные
    final_html = template_content.replace("__DATA_PLACEHOLDER__", js_data)

    # Сохраняем результат в index.html, который и отображает GitHub Pages
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ index.html успешно сгенерирован на основе актуального watchlist.txt!")

if __name__ == "__main__":
    build_dashboard()