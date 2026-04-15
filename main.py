import os
import requests
from datetime import datetime
import json
from analyzers.market_structure import MarketStructureAnalyzer
from analyzers.multi_timeframe import MultiTimeframeAnalyzer
from analyzers.harmonic_patterns import HarmonicPatternAnalyzer
from analyzers.price_action_blocks import PriceActionAnalyzer
from signals.signal_generator import SignalGenerator

# Configuration
TELEGRAM_BOT_TOKEN = "8728759391:AAHWoSWrVMg_VP2yi2P-f-RERefQG-eMeuY"
TELEGRAM_CHAT_ID = "-5196400496"

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
        print(f"✅ Message sent: {message[:50]}...")
    except Exception as e:
        print(f"❌ Error sending message: {e}")

def format_signal_message(signal_data):
    """Format signal data for Telegram"""
    
    symbol = signal_data.get("symbol", "UNKNOWN")
    signal = signal_data.get("signal", "WAIT")
    confidence = signal_data.get("confidence", 0)
    tier = signal_data.get("tier", "UNKNOWN")
    
    if signal == "WAIT":
        reason = signal_data.get("reason", "No setup")
        return f"⏳ {symbol}: WAIT ({confidence}%) - {reason}"
    
    entry = signal_data.get("entry", 0)
    tp1 = signal_data.get("tp1", 0)
    tp2 = signal_data.get("tp2", 0)
    tp3 = signal_data.get("tp3", 0)
    sl = signal_data.get("sl", 0)
    rr = signal_data.get("risk_reward", 0)
    confluence = signal_data.get("confluence", [])
    
    emoji = "🟢" if signal == "LONG" else "🔴"
    
    message = f"""{emoji} <b>{symbol} - {signal}</b>

📊 <b>Tier:</b> {tier}
📈 <b>Confidence:</b> {confidence}%

💰 <b>Entry:</b> {entry:.2f}
🎯 <b>TP1:</b> {tp1:.2f}
🎯 <b>TP2:</b> {tp2:.2f}
🎯 <b>TP3:</b> {tp3:.2f}
🛑 <b>SL:</b> {sl:.2f}

📋 <b>R:R:</b> 1:{rr:.1f}

✅ <b>Confluence:</b>
"""
    
    for item in confluence:
        message += f"  • {item}\n"
    
    message += f"\n⏰ {datetime.now().strftime('%H:%M:%S')}"
    
    return message

def analyze_symbol(symbol, prices_4h, prices_1h, volumes_1h, current_price):
    """Analyze single symbol across all timeframes"""
    
    try:
        # Initialize analyzers
        ms_analyzer = MarketStructureAnalyzer(prices_4h)
        mtf_analyzer = MultiTimeframeAnalyzer(prices_1h)
        harmonic_analyzer = HarmonicPatternAnalyzer(prices_4h)
        pa_analyzer = PriceActionAnalyzer(prices_1h, volumes_1h)
        signal_gen = SignalGenerator(min_confidence=90)
        
        # Run analysis
        ms_result = ms_analyzer.analyze(current_price)
        mtf_result = mtf_analyzer.analyze(current_price)
        harmonic_result = harmonic_analyzer.analyze()
        pa_result = pa_analyzer.analyze(current_price)
        volume_result = pa_result.get("volume", {})
        
        # Generate signal
        signal = signal_gen.generate_signal(
            symbol=symbol,
            market_structure=ms_result,
            multi_timeframe=mtf_result,
            harmonic=harmonic_result,
            price_action=pa_result,
            current_price=current_price,
            volume=volume_result
        )
        
        return signal
    
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
        return None

def main():
    """Main trading agent loop"""
    
    print("🚀 Kenan VİOP Ajanları Started")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Monitoring {len(SYMBOLS)} symbols")
    print("\n📋 SYMBOLS:")
    for symbol in SYMBOLS:
        print(f"   • {symbol}")
    
    # Send startup message
    startup_msg = f"""🕵️‍♂️ <b>Kenan VİOP Ajanları</b>

🔍 <b>Analiz edildi: {len(SYMBOLS)} Hisse</b>

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    for i, symbol in enumerate(SYMBOLS, 1):
        startup_msg += f"{i}. {symbol}\n"
    
    startup_msg += f"""
<b>Durumu:</b> ✅ HAZIR
<b>Sonraki Tarama:</b> Her 4 Saate
<b>Minimum Güven:</b> 90%
<b>Risk/Reward:</b> Min 1:2"""
    
    send_telegram_message(startup_msg)
    
    print("\n✅ Agent running successfully!")
    print("⏳ Waiting for market data...")
    print("📡 Ready to send signals when conditions are MET (90%+ confidence only)")

if __name__ == "__main__":
    main()

