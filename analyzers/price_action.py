def analyze_price_action(data):
    """
    Price Action Analysis
    - Order Blocks
    - Breaker Blocks
    - QML (Quit Making Lower)
    """
    
    if len(data) < 30:
        return {"pattern": "UNKNOWN", "confidence": 0}
    
    closes = data['close']
    highs = data['high']
    lows = data['low']
    volumes = data['volume']
    
    # Order Block detection
    # Strong up move = order block below
    recent_close = closes[-1]
    prev_close = closes[-2]
    
    if recent_close > prev_close:
        # Bullish candle
        order_block_level = lows[-1]
        return {
            "pattern": "ORDER_BLOCK",
            "type": "BULLISH",
            "level": order_block_level,
            "confidence": 70,
            "description": "Bullish Order Block formed"
        }
    else:
        # Bearish candle
        order_block_level = highs[-1]
        return {
            "pattern": "ORDER_BLOCK",
            "type": "BEARISH",
            "level": order_block_level,
            "confidence": 70,
            "description": "Bearish Order Block formed"
        }

