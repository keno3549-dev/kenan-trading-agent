from flask import Flask, request
from signals.signal_generator import SignalGenerator
import json
from datetime import datetime
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8728759391:AAHWoSWrVMg_VP2yi2P-f-RERefQG-eMeuY"
TELEGRAM_CHAT_ID = "-5196400496"

@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    """Receive alert from TradingView"""
    
    try:
        data = request.json
        
        print(f"✅ Alert received: {data}")
        
        # Extract data
        symbol = data.get("symbol", "UNKNOWN")
        close = float(data.get("close", 0))
        volume = float(data.get("volume", 0))
        
        # Send to Telegram
        message = f"""📊 <b>TradingView Alert</b>

Symbol: {symbol}
Price: {close}
Volume: {volume}
Time: {datetime.now().strftime('%H:%M:%S')}"""
        
        send_telegram(message)
        
        return {"status": "received", "symbol": symbol}, 200
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}, 400

def send_telegram(message):
    """Send to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

