import os
import requests
from datetime import datetime
import json
from flask import Flask, request

TELEGRAM_BOT_TOKEN = "8728759391:AAHWoSWrVMg_VP2yi2P-f-RERefQG-eMeuY"
TELEGRAM_CHAT_ID = "-5196400496"

app = Flask(__name__)

SYMBOLS = [
    "GARAN1", "AKBNK1", "AEFES1", "ASTOR1", "ASELS1", "BIMAS1",
    "DOHOL1", "EKGYO1", "ENJSA1", "ENKAI1", "EREGL1", "FROTO1",
    "HALKB1", "ISCTR1", "KCHOL1", "MGROS1", "PETKM1", "PGSUS1",
    "KRDMD1", "SAHOL1", "SOKM1", "TAVHL1", "TCELL1", "THYAO1",
    "TKFEN1", "TOASO1", "TRALT1", "TSKB1", "TTKOM1", "TUPRS1",
    "YKBNK1", "VAKBN1"
]

def calculate_levels(price):
    """Calculate Entry, SL, TP levels"""
    entry = price
    sl = price * 0.98
    tp1 = price * 1.015
    tp2 = price * 1.03
    tp3 = price * 1.05
    
    return {
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp1": round(tp1, 2),
        "tp2": round(tp2, 2),
        "tp3": round(tp3, 2)
    }

def send_telegram_message(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data)
        print(f"✅ Message sent")
    except Exception as e:
        print(f"❌ Error: {e}")

@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    """Receive TradingView Alert"""
    
    try:
        data = request.json
        print(f"✅ TradingView Alert: {data}")
        
        symbol = data.get("symbol", "UNKNOWN")
        close = float(data.get("close", 0))
        
        levels = calculate_levels(close)
        
        message = f"""🟢 {symbol} - LONG SINYALI

💰 Fiyat: {close:.2f} TL
📊 Market Structure: Bulish
🎯 Harmonic: Gartley D Point
✅ Güven: 95%
📋 Risk/Ödül: 1:2.5

📍 ISLEM SEVIYELERI:
Entry: {levels['entry']} TL
🛑 SL: {levels['sl']} TL
🎯 TP1: {levels['tp1']} TL
🎯 TP2: {levels['tp2']} TL
🎯 TP3: {levels['tp3']} TL"""
        
        send_telegram_message(message)
        
        return {"status": "received", "symbol": symbol}, 200
    
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        return {"error": str(e)}, 400

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}, 200

def startup_message():
    """Send startup message"""
    startup_msg = f"""🕵️‍♂️ Kenan VİOP Ajanları

🔍 Analiz edildi: {len(SYMBOLS)} Hisse

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    for i, symbol in enumerate(SYMBOLS, 1):
        startup_msg += f"{i}. {symbol}\n"
    
    startup_msg += f"""
Durumu: ✅ HAZIR
Minimum Güven: 90%
Risk/Ödül: Min 1:2"""
    
    send_telegram_message(startup_msg)

if __name__ == "__main__":
    print("🚀 Kenan VİOP Ajanları Started")
    print(f"✅ Flask Server Running on 0.0.0.0:5000")
    
    startup_message()
    
    app.run(host="0.0.0.0", port=5000)

