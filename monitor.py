import requests
import os

# Variables de entorno
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    print("Telegram:", r.text)

def test_binance():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    r = requests.get(url)
    print("Binance status:", r.status_code)
    print("Binance response:", r.text)
    return r.text

if __name__ == "__main__":
    resp = test_binance()
    send_telegram(f"Respuesta Binance: {resp}")
