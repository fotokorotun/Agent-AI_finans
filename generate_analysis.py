import os
import requests
import yfinance as yf

# Считываем переменные окружения, переданные из GitHub Actions
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram_alert(message):
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Telegram credentials not found, skipping alert.")
    return
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
  try:
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code != 200:
      print(f"Failed to send telegram alert: {response.text}")
  except Exception as e:
    print(f"Error sending telegram alert: {e}")


def check_price_alerts(tickers_list):
  alerts = []
  for ticker in tickers_list:
    try:
      stock = yf.Ticker(ticker)
      hist = stock.history(period="2d")
      if len(hist) >= 2:
        prev_close = hist["Close"].iloc[-2]
        current_price = hist["Close"].iloc[-1]
        change_pct = ((current_price - prev_close) / prev_close) * 100

        # Срабатывает при падении <= -10% ИЛИ росте >= 10%
        if abs(change_pct) >= 10.0:
          emoji = "🚀" if change_pct > 0 else "🔻"
          sign = "+" if change_pct > 0 else ""
          msg = (
              f"{emoji} *{ticker}*: изменение на *{sign}{change_pct:.2f}%*\n"
              f"• Пред. цена: `{prev_close:.2f}`\n"
              f"• Тек. цена: `{current_price:.2f}`"
          )
          alerts.append(msg)
    except Exception as e:
      print(f"Error checking {ticker}: {e}")

  if alerts:
    full_message = (
        "⚠️ *Внимание! Резкое движение в портфеле (>= 10%):*\n\n"
        + "\n\n".join(alerts)
    )
    send_telegram_alert(full_message)