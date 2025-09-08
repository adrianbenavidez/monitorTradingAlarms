import requests
import time
import os
from datetime import datetime, timedelta, timezone


# Quitar comentarios para correr en local
#from dotenv import load_dotenv
#load_dotenv()


# --- Zona horaria fija UTC-3 (Argentina sin horario de verano) ---
ARG = timezone(timedelta(hours=-3))


def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response["price"])


def get_24h_stats(symbol):
    """Devuelve variación 24h y volumen"""
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url).json()
    change_percent = float(response["priceChangePercent"])
    volume = float(response["volume"])
    return change_percent, volume


def get_weekly_high_low(symbol):
    """Obtiene máximo y mínimo de los últimos 7 días"""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=7"
    response = requests.get(url).json()
    highs = [float(candle[2]) for candle in response]  # índice 2 = high
    lows = [float(candle[3]) for candle in response]   # índice 3 = low
    return max(highs), min(lows)


# --- Configuración de Telegram ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


# --- Lista de activos con parámetros ---
activos = [
    {"symbol": "SOLUSDT", "max": 295, "min": 153},
    {"symbol": "BTCUSDT", "max": 124000, "min": 93000},
    {"symbol": "ETHUSDT", "max": 4820, "min": 4291},
    {"symbol": "BNBUSDT", "max": 901, "min": 820},
    {"symbol": "XRPUSDT", "max": 3.62, "min": 1.92},
    {"symbol": "ADAUSDT", "max": 1.18, "min": 0.51},
    {"symbol": "DOGEUSDT", "max": 0.43, "min": 0.14},
    {"symbol": "DOTUSDT", "max": 5.35, "min": 3.09},
    {"symbol": "AVAXUSDT", "max": 27, "min": 17},
    {"symbol": "LTCUSDT", "max": 133, "min": 75},
    {"symbol": "PAXGUSDT", "max": 4000, "min": 3628},
    {"symbol": "PAXGUSDT", "max": 4000, "min": 3622},
    {"symbol": "PAXGUSDT", "max": 4000, "min": 3620},
    {"symbol": "PAXGUSDT", "max": 4000, "min": 3612},
    {"symbol": "PAXGUSDT", "max": 4000, "min": 3636},
]

# --- Inicio ---
send_telegram("🚨 Monitoreo iniciado para múltiples activos")

# Variables para controlar mensajes diarios
last_sent_date_8 = None
last_sent_date_21 = None

# --- Loop principal ---
while True:
    for activo in activos:
        symbol = activo["symbol"]
        alerta_max = activo["max"]
        alerta_min = activo["min"]

        try:
            precio = get_price(symbol)
            change_24h, volumen = get_24h_stats(symbol)
            high_week, low_week = get_weekly_high_low(symbol)
            now = datetime.now(ARG).strftime("%d/%m/%Y %H:%M")

            print(f"{symbol} -> {precio}")

            if precio >= alerta_max:
                send_telegram(
                    f"🚀 {symbol} rompió resistencia {alerta_max}\n"
                    f"📈 Precio actual: {precio}\n"
                    f"📊 Variación 24h: {change_24h:.2f}%\n"
                    f"🔼 Máximo semanal: {high_week}\n"
                    f"🔽 Mínimo semanal: {low_week}\n"
                    f"🕒 Hora: {now}"
                )
            elif precio <= alerta_min:
                send_telegram(
                    f"⚠️ {symbol} rompió soporte {alerta_min}\n"
                    f"📉 Precio actual: {precio}\n"
                    f"📊 Variación 24h: {change_24h:.2f}%\n"
                    f"🔼 Máximo semanal: {high_week}\n"
                    f"🔽 Mínimo semanal: {low_week}\n"
                    f"🕒 Hora: {now}"
                )

        except Exception as e:
            print(f"Error obteniendo {symbol}: {e}")

    # --- Heartbeat ---
    now = datetime.now(ARG)
    hora_actual = now.hour
    minuto_actual = now.minute
    fecha_actual = now.date()

    if hora_actual == 8 and minuto_actual == 0 and last_sent_date_8 != fecha_actual:
        send_telegram(
            f"✅ Bot en ejecución (08:00) - {now.strftime('%d/%m/%Y %H:%M')}")
        last_sent_date_8 = fecha_actual

    if hora_actual == 21 and minuto_actual == 0 and last_sent_date_21 != fecha_actual:
        send_telegram(
            f"✅ Bot en ejecución (21:00) - {now.strftime('%d/%m/%Y %H:%M')}")
        last_sent_date_21 = fecha_actual

    time.sleep(60)  # revisa cada minuto
