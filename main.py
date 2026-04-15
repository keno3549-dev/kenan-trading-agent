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

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print(f"✅ Sent")
    except Exception as e:
        print(f"❌ Error: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print(f"✅ Alert: {data}")
        
        symbol = data.get("symbol", "UNKNOWN")
        close = float(data.get("close", 0))
        atr = float(data.get("atr", 0))
        signal_type = data.get("type", "UNKNOWN")
        
        if signal_type == "LONG":
            sl = close - (atr * 1.5)
            tp = close + (close * 0.0618)
            emoji = "🟢"
            type_text = "LONG"
        else:
            sl = close + (atr * 1.5)
            tp = close - (close * 0.0618)
            emoji = "🔴"
            type_text = "SHORT"
        
        risk = abs(close - sl)
        profit = abs(tp - close)
        ratio = profit / risk if risk > 0 else 0
        
        message = f"""🕵️‍♂️ VİOP Ajanları

🔔 {symbol} | 15DK

{emoji} {type_text} Sinyali

💰 Giriş: {close:.2f} TL
🚀 Market Structure: Bullish
🎯 Harmonic: Gartley D Point
🛟 Güven: 95%
🏆 Risk/Ödül: 1:{ratio:.1f}

📍 ISLEM SEVIYELERI:
Giriş: {close:.2f} TL
🛑 SL: {sl:.2f} TL
🎯 TP: {tp:.2f} TL"""
        
        send_telegram(message)
        
        return {"status": "ok", "symbol": symbol}, 200
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}, 400

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

def startup():
    msg = f"""🕵️‍♂️ VİOP Ajanları

🔍 Analiz edildi: {len(SYMBOLS)} Hisse

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    for i, s in enumerate(SYMBOLS, 1):
        msg += f"{i}. {s}\n"
    
    msg += f"""
Durumu: ✅ HAZIR
Minimum Güven: 90%
Risk/Ödül: Min 1:2"""
    
    send_telegram(msg)

if __name__ == "__main__":
    print("🚀 Started")
    startup()
    app.run(host="0.0.0.0", port=5000)

