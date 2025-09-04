import requests
import time
import os
from datetime import datetime, timedelta, timezone

# Quitar comentarios para correr en local
from dotenv import load_dotenv
load_dotenv()

# --- Zona horaria fija UTC-3 (Argentina sin horario de verano) ---
ARG = timezone(timedelta(hours=-3))

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

# Variables para controlar si ya se enviaron los mensajes diarios
last_sent_date_8 = None
last_sent_date_21 = None

# --- Loop principal ---
while True:
    # --- Chequeo de precios ---
    for activo in activos:
        symbol = activo["symbol"]
        alerta_max = activo["max"]
        alerta_min = activo["min"]

        try:
            precio = get_price(symbol)
            print(f"{symbol} -> {precio}")

            if precio >= alerta_max:
                send_telegram(
                    f"🚀 {symbol} alcanzó {precio}, rompió resistencia {alerta_max}"
                )
            elif precio <= alerta_min:
                send_telegram(
                    f"⚠️ {symbol} cayó a {precio}, rompió soporte {alerta_min}"
                )

        except Exception as e:
            print(f"Error obteniendo {symbol}: {e}")

    # --- Chequeo heartbeat (Argentina UTC-3) ---
    now = datetime.now(ARG)
    hora_actual = now.hour
    minuto_actual = now.minute
    fecha_actual = now.date()

    # A las 8:00
    if hora_actual == 8 and minuto_actual == 0 and last_sent_date_8 != fecha_actual:
        send_telegram(
            f"✅ Bot en ejecución (control 08:00) - {now.strftime('%d/%m/%Y %H:%M')}"
        )
        last_sent_date_8 = fecha_actual

    # A las 21:00
    if hora_actual == 21 and minuto_actual == 0 and last_sent_date_21 != fecha_actual:
        send_telegram(
            f"✅ Bot en ejecución (control 21:00) - {now.strftime('%d/%m/%Y %H:%M')}"
        )
        last_sent_date_21 = fecha_actual

    time.sleep(60)  # revisa cada minuto para no perder la hora exacta
