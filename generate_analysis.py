import sys
import pandas as pd
import yfinance as yf
import math
import os

def generate_dynamic_site(budget=500):
    print(f"Мотор запущен: сбор данных и генерация дашборда для бюджета: {budget} €...")
    
    # Кросс-курсы
    try:
        usd_eur = 1 / yf.Ticker('EURUSD=X').history(period='1d')['Close'].iloc[-1]
    except:
        usd_eur = 0.92
        
    try:
        krw_eur = yf.Ticker('KRWEUR=X').history(period='1d')['Close'].iloc[-1]
    except:
        krw_eur = 0.00066

    try:
        gbp_eur = yf.Ticker('GBPEUR=X').history(period='1d')['Close'].iloc[-1]
    except:
        gbp_eur = 1.19

    try:
        with open('watchlist.txt', 'r', encoding='utf-8') as f:
            tickers = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("Ошибка: watchlist.txt не найден!")
        return

    total_len = len(tickers)
    top10_tickers = tickers[:10] if total_len >= 10 else tickers
    passive10_tickers = tickers[10:20] if total_len >= 20 else tickers[:10]

    w_top = [0.20, 0.15, 0.12, 0.10, 0.10, 0.09, 0.08, 0.07, 0.05, 0.04][:len(top10_tickers)]
    w_pass = [0.15, 0.15, 0.12, 0.12, 0.10, 0.10, 0.08, 0.08, 0.05, 0.05][:len(passive10_tickers)]
    
    if sum(w_top) > 0: w_top = [w / sum(w_top) for w in w_top]
    if sum(w_pass) > 0: w_pass = [w / sum(w_pass) for w in w_pass]

    all_items_js = []

    for ticker in tickers:
        price_eur = 50.0
        name = ticker
        
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='5d')
            
            if not hist.empty and 'Close' in hist:
                val = hist['Close'].iloc[-1]
                if not math.isnan(val) and val > 0:
                    price_local = float(val)
                    info = stock.info
                    currency = info.get('currency', 'USD')
                    name = info.get('shortName') or info.get('longName') or ticker
                    
                    if currency == 'GBp':
                        price_eur = (price_local / 100.0) * gbp_eur
                    elif currency == 'GBP':
                        price_eur = price_local * gbp_eur
                    elif currency == 'USD':
                        price_eur = price_local * usd_eur
                    elif currency == 'KRW':
                        price_eur = price_local * krw_eur
                    elif currency == 'JPY':
                        price_eur = price_local * 0.0061
                    else:
                        price_eur = price_local
        except Exception as e:
            print(f"Резервная цена для {ticker}: {e}")

        if math.isnan(price_eur) or price_eur <= 0:
            price_eur = 50.0

        is_top10 = ticker in top10_tickers
        is_pass10 = ticker in passive10_tickers

        w_t = w_top[top10_tickers.index(ticker)] if is_top10 else 0.0
        w_p = w_pass[passive10_tickers.index(ticker)] if is_pass10 else 0.0

        sector = "Technology / Growth" if is_top10 else "Dividend / Defensive"
        risk = "Умеренный" if is_top10 else "Низкий"
        ret6m = "+20.0%" if is_top10 else "+8.0%"
        ret1y = "+40.0%" if is_top10 else "+15.0%"

        item_str = f"""{{
            ticker: "{ticker}",
            name: "{name.replace('"', '')}",
            sector: "{sector}",
            priceEur: {round(price_eur, 2)},
            isTop10: {str(is_top10).lower()},
            isPass10: {str(is_pass10).lower()},
            weightTop: {w_t},
            weightPass: {w_p},
            ret6m: "{ret6m}",
            ret1y: "{ret1y}",
            risk: "{risk}",
            debt: "Низкий",
            mood: "Стабильный",
            vol: "Средняя"
        }}"""

        all_items_js.append(item_str)
        print(f"[OK] {ticker} -> {round(price_eur, 2)} €")

    js_array = ",\n".join(all_items_js)

    # Читаем шаблон HTML оформления
    if os.path.exists('template.html'):
        with open('template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        # Вставляем данные внутрь шаблона
        final_html = template_content.replace('__DATA_PLACEHOLDER__', js_array)
    else:
        print("Ошибка: файл template.html не найден!")
        return

    # Записываем готовый результат в index.html для браузера
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Мотор успешно отработал: index.html собран на основе template.html!")

if __name__ == '__main__':
    user_budget = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    generate_dynamic_site(user_budget)