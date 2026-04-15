import subprocess
import json
import sys

def get_tradingview_data(symbol, timeframe="15"):
    """
    TradingView MCP Jackson'dan veri çek
    """
    try:
        # MCP request (mock - gerçek implementasyon sonra)
        print(f"🔍 Fetching {symbol} {timeframe}min...")
        
        # Simulated response
        data = {
            'symbol': symbol,
            'timeframe': timeframe,
            'close': 142.50,
            'high': 143.20,
            'low': 141.80,
            'volume': 1250000,
            'atr': 0.95
        }
        
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "GARAN1"
    data = get_tradingview_data(symbol)
    print(json.dumps(data, indent=2))

