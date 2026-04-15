def analyze_market_structure(data):
    """
    Market Structure Analysis
    - HH/HL (Uptrend)
    - LH/LL (Downtrend)
    - Consolidation
    """
    
    if len(data) < 20:
        return {"trend": "UNKNOWN", "confidence": 0}
    
    closes = data['close']
    highs = data['high']
    lows = data['low']
    
    # Last 5 bars
    recent_highs = highs[-5:]
    recent_lows = lows[-5:]
    
    # HH/HL detection (Uptrend)
    if recent_highs[-1] > recent_highs[-3]:
        if recent_lows[-1] > recent_lows[-3]:
            return {
                "trend": "BULLISH",
                "pattern": "HH/HL",
                "confidence": 85,
                "description": "Higher High, Higher Low"
            }
    
    # LH/LL detection (Downtrend)
    if recent_highs[-1] < recent_highs[-3]:
        if recent_lows[-1] < recent_lows[-3]:
            return {
                "trend": "BEARISH",
                "pattern": "LH/LL",
                "confidence": 85,
                "description": "Lower High, Lower Low"
            }
    
    # Consolidation
    return {
        "trend": "CONSOLIDATION",
        "pattern": "NEUTRAL",
        "confidence": 50,
        "description": "No clear direction"
    }

