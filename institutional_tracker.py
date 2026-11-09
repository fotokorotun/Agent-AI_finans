import sys
import yfinance as yf

def generate_institutional_tracker():
    print("Сканирование институциональных потоков и фондов...")
    
    try:
        with open('institutional_watchlist.txt', 'r', encoding='utf-8') as f:
            tickers = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("Ошибка: institutional_watchlist.txt не найден!")
        return

    # Карта регионального и институционального анализа
    asset_profiles = {
        "BLK": {"name": "BlackRock, Inc.", "type": "Управляющий фондами", "region": "США", "flow": "Приток в приватный кредит / ИИ"},
        "STT": {"name": "State Street Corp.", "type": "Кастодиан / Фонды", "region": "США", "flow": "Стабильный ребаланс"},
        "BK": {"name": "The Bank of New York Mellon", "type": "Институциональный банк", "region": "США", "flow": "Накопление активов"},
        "TROW": {"name": "T. Rowe Price Group", "type": "Инвестиционный фонд", "region": "США", "flow": "Ротация в технологический сектор"},
        "SPY": {"name": "SPDR S&P 500 ETF Trust", "type": "Флагманский ETF", "region": "США", "flow": "Основной приток ликвидности"},
        "IVV": {"name": "iShares Core S&P 500 ETF (BlackRock)", "type": "Институциональный ETF", "region": "США", "flow": "Долгосрочный капитал пенсий"},
        "VGK": {"name": "Vanguard FTSE Europe ETF", "type": "Региональный ETF", "region": "Европа", "flow": "Умеренный приток (дешевые оценки)"},
        "VPL": {"name": "Vanguard FTSE Pacific ETF", "type": "Региональный ETF", "region": "Азия-Тихий океан", "flow": "Перелив капитала в Японию и Сингапур"},
        "EWU": {"name": "iShares MSCI United Kingdom ETF", "type": "Страновой ETF", "region": "Англия", "flow": "Защитные дивидендные потоки"},
        "EZU": {"name": "iShares MSCI Eurozone ETF", "type": "Страновой ETF", "region": "Европа", "flow": "Ребалансировка в промышленные циклы"},
        "MCHI": {"name": "iShares MSCI China ETF", "type": "Страновой ETF", "region": "Азия (Китай)", "flow": "Спекулятивный приток / Выход"},
        "XLE": {"name": "Energy Select Sector SPDR", "type": "Секторный ETF", "region": "США", "flow": "Хеджирование инфляции"},
        "XLF": {"name": "Financial Select Sector SPDR", "type": "Секторный ETF", "region": "США", "flow": "Институциональный переток"}
    }

    html_rows = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1mo')
            price = hist['Close'].iloc[-1] if not hist.empty else 100.0
            prev_price = hist['Close'].iloc[0] if not hist.empty else price
            monthly_change = ((price - prev_price) / prev_price) * 100
            
            profile = asset_profiles.get(ticker, {"name": ticker, "type": "Инструмент / Акция", "region": "Глобальный", "flow": "Мониторинг потоков"})
            
            trend_color = "text-emerald-400" if monthly_change >= 0 else "text-rose-400"
            change_sign = "+" if monthly_change >= 0 else ""

            html_rows.append(f"""
                <tr class="hover:bg-gray-800/40 transition-colors">
                    <td class="p-3 font-mono font-bold text-emerald-400">{ticker} <span class="block text-xs font-normal text-gray-400">{profile['name']}</span></td>
                    <td class="p-3 text-gray-300">{profile['type']}</td>
                    <td class="p-3 font-semibold text-blue-300">{profile['region']}</td>
                    <td class="p-3 font-mono">{price:.2f} $</td>
                    <td class="p-3 font-mono font-bold {trend_color}">{change_sign}{monthly_change:.2f}%</td>
                    <td class="p-3 text-xs text-gray-300">{profile['flow']}</td>
                </tr>
            """)
            print(f"[Институт] Обработано: {ticker} ({profile['region']})")
        except Exception as e:
            print(f"Ошибка по {ticker}: {e}")

    rows_str = "".join(html_rows)

    dashboard_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Institutional Capital Flows Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #0b0f19; color: #f3f4f6; font-family: sans-serif; }}
        .card-bg {{ background-color: #111827; border: 1px solid #1f2937; }}
    </style>
</head>
<body class="p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <header class="flex justify-between items-center pb-6 border-b border-gray-800">
            <div>
                <h1 class="text-2xl font-bold text-white flex items-center gap-2">
                    🏛️ Institutional Capital Tracker (BlackRock, Vanguard & Flows)
                </h1>
                <p class="text-sm text-gray-400 mt-1">Мониторинг перелива капитала институционалов по регионам: США, Европа, Азия, Англия</p>
            </div>
            <div class="card-bg p-3 rounded-xl">
                <span class="text-xs text-emerald-400 font-bold uppercase tracking-wider">Статус: Активный сканер</span>
            </div>
        </header>

        <!-- Региональный срез потоков -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="card-bg p-4 rounded-xl border-t-2 border-emerald-500">
                <div class="text-xs text-gray-400 uppercase font-semibold">США (Технологии & AI)</div>
                <div class="text-lg font-bold text-white mt-1">Основной приток</div>
                <div class="text-xs text-emerald-400 mt-1">Фокус: BlackRock / Флагманские ETF</div>
            </div>
            <div class="card-bg p-4 rounded-xl border-t-2 border-blue-500">
                <div class="text-xs text-gray-400 uppercase font-semibold">Европа (Дивиденды / Value)</div>
                <div class="text-lg font-bold text-white mt-1">Умеренный приток</div>
                <div class="text-xs text-blue-400 mt-1">Фокус: VGK, EZU, UK активы</div>
            </div>
            <div class="card-bg p-4 rounded-xl border-t-2 border-amber-500">
                <div class="text-xs text-gray-400 uppercase font-semibold">Азия (Япония / Сингапур)</div>
                <div class="text-lg font-bold text-white mt-1">Переток капитала</div>
                <div class="text-xs text-amber-400 mt-1">Фокус: VPL, японские реструктуризации</div>
            </div>
            <div class="card-bg p-4 rounded-xl border-t-2 border-purple-500">
                <div class="text-xs text-gray-400 uppercase font-semibold">Англия (Защитные активы)</div>
                <div class="text-lg font-bold text-white mt-1">Стабильные потоки</div>
                <div class="text-xs text-purple-400 mt-1">Фокус: EWU, дивидендные лидеры LSE</div>
            </div>
        </div>

        <!-- Таблица институциональных активов -->
        <div class="card-bg rounded-xl overflow-hidden shadow-xl">
            <div class="p-4 border-b border-gray-800 font-semibold text-white">Таблица институционального мониторинга и динамики</div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-sm">
                    <thead>
                        <tr class="border-b border-gray-800 text-xs text-gray-400 uppercase bg-gray-900/50">
                            <th class="p-3">Тикер / Фонд</th>
                            <th class="p-3">Тип структуры</th>
                            <th class="p-3">Регион фокуса</th>
                            <th class="p-3">Цена ($)</th>
                            <th class="p-3">Динамика (1M)</th>
                            <th class="p-3">Направление капитала (Flow)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-800">
                        {rows_str}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Институциональный чек-лист и отчет -->
        <div class="card-bg p-6 rounded-xl space-y-4">
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
                📋 Чек-лист и регламент отчетов: Как отслеживать действия фондов
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-gray-300">
                <div class="bg-gray-900/50 p-4 rounded-lg space-y-2 border border-gray-800">
                    <div class="font-bold text-emerald-400 text-sm">1. Отчеты 13F (США)</div>
                    <p>Публикуются раз в квартал (через 45 дней после окончания квартала). Проверяйте сайты WhaleWisdom или SEC EDGAR для BlackRock (BLK) и Vanguard, чтобы видеть новые топ-покупки.</p>
                </div>
                <div class="bg-gray-900/50 p-4 rounded-lg space-y-2 border border-gray-800">
                    <div class="font-bold text-blue-400 text-sm">2. Еженедельные ETF Flows</div>
                    <p>Следите за притоками в фонды `VGK` (Европа) и `VPL` (Азия) на ETF.com. Резкий рост притока означает крупную ребалансировку институционалов в эти регионы.</p>
                </div>
                <div class="bg-gray-900/50 p-4 rounded-lg space-y-2 border border-gray-800">
                    <div class="font-bold text-amber-400 text-sm">3. Инсайдерские реестры (UK / SG)</div>
                    <p>Для британских (`.L`) и сингапурских (`.SI`) компаний крупные фонды обязаны раскрывать превышение порога в 3-5% голосующих акций. Отслеживайте их через Financial Times.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open('institutional_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

    print("Институциональный дашборд успешно сгенерирован в файл institutional_dashboard.html!")

if __name__ == '__main__':
    generate_institutional_tracker()