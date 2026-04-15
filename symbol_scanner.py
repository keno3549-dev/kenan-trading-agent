import requests
import json
from datetime import datetime
from analyzers.market_structure import analyze_market_structure
from analyzers.harmonic_patterns import analyze_harmonic_patterns
from analyzers.price_action import analyze_price_action
from analyzers.confluence_scorer import score_confluence

SYMBOLS = [
    "GARAN1", "AKBNK1", "AEFES1", "ASTOR1", "ASELS1", "BIMAS1",
    "DOHOL1", "EKGYO1", "ENJSA1", "ENKAI1", "EREGL1", "FROTO1",
    "HALKB1", "ISCTR1", "KCHOL1", "MGROS1", "PETKM1", "PGSUS1",
    "KRDMD1", "SAHOL1", "SOKM1", "TAVHL1", "TCELL1", "THYAO1",
    "TKFEN1", "TOASO1", "TRALT1", "TSKB1", "TTKOM1", "TUPRS1",
    "YKBNK1", "VAKBN1"
]

TELEGRAM_BOT_TOKEN = "8728759391:AAHWoSWrVMg_VP2yi2P-f-RERefQG-eMeuY"
TELEGRAM_CHAT_ID = "-5196400496"

def get_symbol_data(symbol):
    """
    Simulated data (TradingView'dan gerçek veri gelecek)
    """
    base_price = {
        "GARAN1": 142.50, "AKBNK1": 79.50, "AEFES1": 19.05,
        "ASTOR1": 20.10, "ASELS1": 416.10, "BIMAS1": 763.70,
        "DOHOL1": 22.18, "EKGYO1": 21.38, "ENJSA1": 7.50,
        "ENKAI1": 13.50, "EREGL1": 28.95, "FROTO1": 25.30,
        "HALKB1": 35.60, "ISCTR1": 49.50, "KCHOL1": 75.80,
        "MGROS1": 42.15, "PETKM1": 59.90, "PGSUS1": 302.50,
        "KRDMD1": 55.20, "SAHOL1": 33.40, "SOKM1": 35.50,
        "TAVHL1": 45.80, "TCELL1": 38.90, "THYAO1": 8.50,
        "TKFEN1": 32.10, "TOASO1": 36.70, "TRALT1": 15.40,
        "TSKB1": 8.45, "TTKOM1": 78.50, "TUPRS1": 125.80,
        "YKBNK1": 12.60, "VAKBN1": 9.80
    }
    
    price = base_price.get(symbol, 100)
    atr = price * 0.015  # %1.5 ATR
    
    # Mock candlestick data
    return {
        'symbol': symbol,
        'close': [price - 2, price - 1.5, price - 1, price - 0.5, price],
        'high': [price + 0.5, price + 0.3, price + 0.2, price + 0.4, price + 0.1],
        'low': [price - 0.5, price - 0.3, price - 0.2, price - 0.4, price - 0.1],
        'volume': [1000000, 1100000, 950000, 1050000, 1200000],
        'atr': atr,
        'price': price
    }

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print(f"✅ Sent: {message[:50]}")
    except Exception as e:
        print(f"❌ Error: {e}")

def scan_symbols():
    """
    32 Symbol'ü tara, signal bul
    """
    signals = []
    
    print(f"🔍 Scanning 32 symbols... {datetime.now().strftime('%H:%M:%S')}")
    
    for symbol in SYMBOLS:
        data = get_symbol_data(symbol)
        
        # Analyze
        ms = analyze_market_structure(data)
        harmonic = analyze_harmonic_patterns(data)
        pa = analyze_price_action(data)
        conf = score_confluence(ms, harmonic, pa, data['atr'])
        
        # 90%+ confidence filter
        if conf.get('confidence', 0) >= 90:
            signals.append({
                'symbol': symbol,
                'confidence': conf.get('confidence'),
                'trend': ms.get('trend'),
                'pattern': harmonic.get('pattern')
            })
            print(f"🔔 SIGNAL: {symbol} | Confidence: {conf.get('confidence'):.0f}%")
    
    return signals

def run_scanner():
    """
    Sürekli tarama (her 15DK)
    """
    signals = scan_symbols()
    
    if signals:
        msg = f"""🕵️‍♂️ VİOP Ajanları - Scan Sonuçları

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔔 SİNYAL SAYISI: {len(signals)}

"""
        for sig in signals:
            msg += f"• {sig['symbol']} | {sig['trend']} | {sig['confidence']:.0f}%\n"
        
        send_telegram(msg)
    else:
        print("❌ No signals found")

if __name__ == "__main__":
    run_scanner()

