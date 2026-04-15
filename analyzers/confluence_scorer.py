def score_confluence(market_structure, harmonic, price_action, atr):
    """
    Confluence Scoring
    - Market Structure: +30 points
    - Harmonic Pattern: +40 points
    - Price Action: +30 points
    - Total: 90+ = SIGNAL
    """
    
    score = 0
    details = []
    
    # Market Structure score
    if market_structure.get("trend") == "BULLISH":
        score += 30
        details.append("MS: Bullish +30")
    elif market_structure.get("trend") == "BEARISH":
        score += 30
        details.append("MS: Bearish +30")
    else:
        score += 10
        details.append("MS: Neutral +10")
    
    # Harmonic score
    if harmonic.get("pattern") != "NONE":
        score += 40
        details.append(f"Harmonic: {harmonic.get('pattern')} +40")
    else:
        score += 5
        details.append("Harmonic: None +5")
    
    # Price Action score
    if price_action.get("pattern") == "ORDER_BLOCK":
        score += 30
        details.append("PA: Order Block +30")
    else:
        score += 10
        details.append("PA: Weak +10")
    
    return {
        "total_score": score,
        "confidence": min(score, 100),
        "is_signal": score >= 90,
        "details": details
    }

