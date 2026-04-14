import os
import requests
from datetime import datetime
import json

# Configuration
TELEGRAM_BOT_TOKEN = "8728759391:AAHWoSWrVMg_VP2yi2P-f-RERefQG-eMeuY"
TELEGRAM_CHAT_ID = "-5196400496"

SYMBOLS = [
    "GARAN1", "AKBNK1", "AEFES1", "AKSEN1", "ASTOR1", "ALARK1",
    "ARCLK1", "ASELS1", "BIMAS1", "BRSAN1", "CIMSA1", "DOAS1",
    "DOHOL1", "EKGYO1", "ELCBASY1", "ENJSA1", "ENKAI1", "EREGL1",
    "FROTO1", "GBPUSD1", "GUBRF1", "HALKB1", "HEKTS1", "ISCTR1",
    "KCHOL1", "KONTR1", "MGROS1", "ODAS1"
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
        print(f"✅ Message sent: {message[:50]}...")
    except Exception as e:
        print(f"❌ Error sending message: {e}")

def analyze_symbols():
    """Analyze all symbols"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"<b>🔍 KENAN BIST TRADING AGENT</b>\n\n"
    message += f"⏰ {timestamp}\n\n"
    message += f"📊 <b>Scanning {len(SYMBOLS)} symbols...</b>\n\n"
    
    for symbol in SYMBOLS:
        message += f"✓ {symbol}\n"
    
    message += f"\n<b>Status:</b> ✅ READY\n"
    message += f"<b>Next scan:</b> Tomorrow 08:00"
    
    return message

def main():
    """Main function"""
    print("🚀 Kenan BIST Trading Agent Started")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Monitoring {len(SYMBOLS)} symbols")
    
    # Test message
    test_message = analyze_symbols()
    send_telegram_message(test_message)
    
    print("✅ Agent running successfully!")

if __name__ == "__main__":
    main()
