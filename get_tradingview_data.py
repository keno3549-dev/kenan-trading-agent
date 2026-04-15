import subprocess
import json
import sys

def get_symbol_data(symbol, timeframe="15"):
    """
    TradingView MCP Jackson'dan veri çek
    """
    try:
        # MCP Jackson komutu
        cmd = f"npm run mcp:request -- 'get-candles' '{symbol}' '{timeframe}'"
        result = subprocess.run(cmd, shell=True, cwd="~/tradingview-mcp-jackson", capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
        else:
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "GARAN1"
    data = get_symbol_data(symbol)
    print(json.dumps(data, indent=2))

