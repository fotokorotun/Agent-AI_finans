import yfinance as yf
import pandas as pd

# Полный ваш список тикеров
tickers_map = {
    'PAM': 'Pampa Energia (GDR)',
    'VEST': 'Vest U.S.',
    'GOOGL': 'Alphabet (A)',
    'ORCL': 'Oracle',
    'NEO.TO': 'Neo Performance Materials',
    'KAP.L': 'Kazatomprom (GDR)',
    'VIST': 'Vista Energy (ADR)',
    'PLTR': 'Palantir Technologies',
    'LEU': 'Centrus Energy (A)',
    'NVDA': 'NVIDIA',
    'SpaceX (Private)': 'SpaceX',
    'CEG': 'Constellation Energy',
    'TMUS': 'T-Mobile US',
    'MP': 'MP Materials',
    'CCJ': 'Cameco',
    'DTEGY': 'Deutsche Telekom',
    'FN': 'Fabrinet',
    'T': 'AT&T',
    'UUUU': 'Energy Fuels',
    'PNG.V': 'Kraken Robotics',
    'NBIS': 'Nebius Group (A)',
    'TSM': 'TSMC (ADR)',
    'MU': 'Micron Technology',
    'GLW': 'Corning',
    'CoreWeave (Private)': 'CoreWeave',
    'AAOI': 'Applied Optoelectronics',
    '005935.KS': 'Samsung (Pref GDR)',
    'WDC': 'SanDisk / Western Digital',
    '000660.KS': 'SK Hynix (GDR)',
    '285A.T': 'Kioxia Holdings'
}

data = []

print("Начинаем скачивание актуальных данных по всем активам...")

for ticker, name in tickers_map.items():
    if 'Private' in ticker:
        data.append({
            'Ticker': ticker, 'Name': name,
            'Trailing P/E': 'N/A', 'Forward P/E': 'N/A',
            'EV/EBITDA': 'N/A', 'Free Cash Flow': 'Private'
        })
        continue

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        t_pe = info.get('trailingPE')
        f_pe = info.get('forwardPE')
        ev_eb = info.get('enterpriseToEbitda')
        fcf = info.get('freeCashflow')

        data.append({
            'Ticker': ticker,
            'Name': info.get('longName', name),
            'Trailing P/E': round(t_pe, 2) if t_pe else None,
            'Forward P/E': round(f_pe, 2) if f_pe else None,
            'EV/EBITDA': round(ev_eb, 2) if ev_eb else None,
            'Free Cash Flow': f"{fcf:,.0f}" if fcf else None
        })
        print(f"[OK] Загружено: {ticker}")
    except Exception as e:
        print(f"[Ошибка] Не удалось загрузить {ticker}: {e}")
        data.append({
            'Ticker': ticker, 'Name': name,
            'Trailing P/E': None, 'Forward P/E': None,
            'EV/EBITDA': None, 'Free Cash Flow': None
        })

df = pd.DataFrame(data)

# Запись в research.md
markdown_table = df.to_markdown(index=False)
with open('research.md', 'w', encoding='utf-8') as f:
    f.write("# Полный актуальный отчет по активам (Research Data)\n\n")
    f.write(markdown_table)

print("\n Готово! Все реальные данные записаны в research.md.")