import requests
import json
from datetime import datetime
from analyzers.market_structure import analyze_market_structure
from analyzers.harmonic_patterns import analyze_harmonic_patterns
from analyzers.price_action import analyze_price_action
from analyzers.confluence_scorer import score_confluence
from tradingview_fetcher import get_tradingview_data

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

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print(f"✅ Sent")
    except Exception as e:
        print(f"❌ Error: {e}")

def get_symbol_data(symbol):
    tv_data = get_tradingview_data(symbol)
    
    if not tv_data:
        return None
    
    close = tv_data.get('close', 100)
    atr = tv_data.get('atr', 1.5)
    
    return {
        'symbol': symbol,
        'close': [close - 2, close - 1.5, close - 1, close - 0.5, close],
        'high': [close + 0.5, close + 0.3, close + 0.2, close + 0.4, close + 0.1],
        'low': [close - 0.5, close - 0.3, close - 0.2, close - 0.4, close - 0.1],
        'volume': [1000000, 1100000, 950000, 1050000, 1200000],
        'atr': atr,
        'price': close
    }

def scan_symbols(min_confidence=60):
    """32 Symbol'ü tara"""
    signals = []
    
    print(f"🔍 Scanning 32 symbols (min: {min_confidence}%)...")
    
    for symbol in SYMBOLS:
        data = get_symbol_data(symbol)
        
        if not data:
            continue
        
        ms = analyze_market_structure(data)
        harmonic = analyze_harmonic_patterns(data)
        pa = analyze_price_action(data)
        conf = score_confluence(ms, harmonic, pa, data['atr'])
        
        confidence = conf.get('confidence', 0)
        print(f"  {symbol}: {confidence:.0f}%")
        
        if confidence >= min_confidence:
            signals.append({
                'symbol': symbol,
                'confidence': confidence,
                'trend': ms.get('trend'),
                'pattern': harmonic.get('pattern')
            })
    
    return signals

if __name__ == "__main__":
    signals = scan_symbols(min_confidence=60)
    print(f"\n✅ Total signals (60%+): {len(signals)}")
    for sig in signals:
        print(f"  • {sig['symbol']} | {sig['confidence']:.0f}% | {sig['trend']}")

