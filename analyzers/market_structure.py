import numpy as np
from typing import List, Dict, Tuple

class MarketStructureAnalyzer:
    """4H Market Structure Analysis (HH/HL vs LH/LL)"""
    
    def __init__(self, prices: List[float], lookback: int = 100):
        self.prices = np.array(prices[-lookback:])
        self.lookback = lookback
    
    def find_swing_points(self, window: int = 5) -> List[Tuple[int, float, str]]:
        """Find local highs and lows (swing points)"""
        points = []
        
        for i in range(window, len(self.prices) - window):
            # Local high
            if self.prices[i] == max(self.prices[i-window:i+window+1]):
                points.append((i, self.prices[i], "HIGH"))
            
            # Local low
            elif self.prices[i] == min(self.prices[i-window:i+window+1]):
                points.append((i, self.prices[i], "LOW"))
        
        return points
    
    def detect_market_structure(self, points: List) -> Dict:
        """Detect HH/HL (uptrend) or LH/LL (downtrend)"""
        
        if len(points) < 4:
            return {"detected": False, "structure": "UNKNOWN"}
        
        # Last 4 points
        recent = points[-4:]
        
        # Extract highs and lows
        highs = [p[1] for p in recent if p[2] == "HIGH"]
        lows = [p[1] for p in recent if p[2] == "LOW"]
        
        if len(highs) < 2 or len(lows) < 2:
            return {"detected": False, "structure": "UNKNOWN"}
        
        # Check for HH/HL (uptrend)
        if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
            return {
                "detected": True,
                "structure": "UPTREND",
                "pattern": "HH/HL",
                "last_high": highs[-1],
                "last_low": lows[-1],
                "bias": "LONG"
            }
        
        # Check for LH/LL (downtrend)
        elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
            return {
                "detected": True,
                "structure": "DOWNTREND",
                "pattern": "LH/LL",
                "last_high": highs[-1],
                "last_low": lows[-1],
                "bias": "SHORT"
            }
        
        else:
            return {"detected": False, "structure": "RANGE"}
    
    def detect_break_of_structure(self, current_price: float, structure: Dict) -> Dict:
        """Detect Break of Structure (BOS)"""
        
        if not structure["detected"]:
            return {"bos": False, "direction": None}
        
        is_uptrend = structure["structure"] == "UPTREND"
        
        if is_uptrend:
            # BOS up: price breaks above last high
            if current_price > structure["last_high"] * 1.001:
                return {
                    "bos": True,
                    "direction": "UP",
                    "level": structure["last_high"],
                    "signal": "LONG"
                }
            # BOS down: price breaks below last low
            elif current_price < structure["last_low"] * 0.999:
                return {
                    "bos": True,
                    "direction": "DOWN",
                    "level": structure["last_low"],
                    "signal": "SHORT"
                }
        else:  # Downtrend
            # BOS down: price breaks below last low
            if current_price < structure["last_low"] * 0.999:
                return {
                    "bos": True,
                    "direction": "DOWN",
                    "level": structure["last_low"],
                    "signal": "SHORT"
                }
            # BOS up: price breaks above last high
            elif current_price > structure["last_high"] * 1.001:
                return {
                    "bos": True,
                    "direction": "UP",
                    "level": structure["last_high"],
                    "signal": "LONG"
                }
        
        return {"bos": False, "direction": None}
    
    def analyze(self, current_price: float) -> Dict:
        """Main market structure analysis"""
        
        points = self.find_swing_points()
        structure = self.detect_market_structure(points)
        bos = self.detect_break_of_structure(current_price, structure)
        
        result = {
            "swing_points": len(points),
            "structure": structure,
            "bos": bos,
            "signal": bos["signal"] if bos["bos"] else "WAIT"
        }
        
        return result

