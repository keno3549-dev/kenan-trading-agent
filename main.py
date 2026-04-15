import os
import requests
from datetime import datetime
import json
from flask import Flask, request
from analyzers.market_structure import MarketStructureAnalyzer
from analyzers.multi_timeframe import MultiTimeframeAnalyzer
from analyzers.harmonic_patterns import HarmonicPatternAnalyzer
from analyzers.price_action_blocks import PriceActionAnalyzer
from signals.signal_generator import SignalGenerator
import threading

# Configuration
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
        volume = float(data.get("volume", 0))
        
        message = f"""📊 <b>TradingView Alert Geldi</b>

Symbol: <b>{symbol}</b>
Price: {close}
Volume: {volume}
⏰ {datetime.now().strftime('%H:%M:%S')}

🔍 Analiz edililiyor..."""
        
        send_telegram_message(message)
        
        return {"status": "received", "symbol": symbol}, 200
    
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        return {"error": str(e)}, 400

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}, 200

def startup_message():
    """Send startup message"""
    startup_msg = f"""🕵️‍♂️ <b>Kenan VİOP Ajanları</b>

🔍 <b>Analiz edildi: {len(SYMBOLS)} Hisse</b>

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    for i, symbol in enumerate(SYMBOLS, 1):
        startup_msg += f"{i}. {symbol}\n"
    
    startup_msg += f"""
<b>Durumu:</b> ✅ HAZIR
<b>Mode:</b> 🌐 TradingView Webhook
<b>Minimum Güven:</b> 90%
<b>Risk/Reward:</b> Min 1:2
<b>Port:</b> 5000"""
    
    send_telegram_message(startup_msg)

if __name__ == "__main__":
    print("🚀 Kenan VİOP Ajanları Started")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Monitoring {len(SYMBOLS)} symbols")
    print("\n✅ Flask Server Running on 0.0.0.0:5000")
    print("📡 Waiting for TradingView alerts...")
    
    startup_message()
    
    app.run(host="0.0.0.0", port=5000)

