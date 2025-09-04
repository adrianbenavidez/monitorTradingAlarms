import requests
import time
import os
# Quitar comentarios para correr en local
# from dotenv import load_dotenv
# load_dotenv()

# --- Función para obtener precio ---
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response["price"])


# --- Configuración de Telegram ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


# --- Lista de activos con parámetros ---
activos = [
    {"symbol": "SOLUSDT", "max": 295, "min": 114},
    {"symbol": "BTCUSDT", "max": 124000, "min": 75000},
    {"symbol": "ETHUSDT", "max": 4820, "min": 4000},
    {"symbol": "BNBUSDT", "max": 901, "min": 735},
    {"symbol": "XRPUSDT", "max": 3.62, "min": 1.92},
    {"symbol": "ADAUSDT", "max": 1.18, "min": 0.51},
    {"symbol": "DOGEUSDT", "max": 0.43, "min": 0.14},
    {"symbol": "DOTUSDT", "max": 5.35, "min": 3.09},
    {"symbol": "AVAXUSDT", "max": 27, "min": 16},
    {"symbol": "LTCUSDT", "max": 133, "min": 75},
]

# --- Inicio ---
send_telegram("🚨 Monitoreo iniciado para múltiples activos")

# --- Loop principal ---
while True:
    for activo in activos:
        symbol = activo["symbol"]
        alerta_max = activo["max"]
        alerta_min = activo["min"]

        try:
            precio = get_price(symbol)
            print(f"{symbol} -> {precio}")

            if precio >= alerta_max:
                send_telegram(
                    f"🚀 {symbol} alcanzó {precio}, rompió resistencia {alerta_max}")
            elif precio <= alerta_min:
                send_telegram(
                    f"⚠️ {symbol} cayó a {precio}, rompió soporte {alerta_min}")

        except Exception as e:
            print(f"Error obteniendo {symbol}: {e}")

    time.sleep(120)  # verifica todos los activos cada 10 segundos



