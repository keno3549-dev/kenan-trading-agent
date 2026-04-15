import numpy as np
from typing import List, Dict

class MultiTimeframeAnalyzer:
    """1H Pattern Analysis (RBR, DBD, RBD, DBR)"""
    
    def __init__(self, prices_1h: List[float], lookback: int = 50):
        self.prices = np.array(prices_1h[-lookback:])
        self.lookback = lookback
    
    def find_resistance_support(self, window: int = 10) -> Dict:
        """Find recent resistance and support levels"""
        
        recent = self.prices[-window:]
        resistance = max(recent)
        support = min(recent)
        
        return {
            "resistance": resistance,
            "support": support,
            "range": resistance - support
        }
    
    def detect_rbr_pattern(self, current_price: float, levels: Dict) -> Dict:
        """
        RBR: Resistance Break Retest
        Price breaks above resistance, pulls back, bounces
        """
        
        resistance = levels["resistance"]
        
        # Price broke above resistance
        if current_price > resistance * 1.002:
            # Pullback happening
            if self.prices[-2] < resistance and self.prices[-1] > resistance * 0.998:
                return {
                    "detected": True,
                    "pattern": "RBR",
                    "level": resistance,
                    "signal": "LONG",
                    "entry": current_price,
                    "confidence": 85
                }
        
        return {"detected": False, "pattern": "RBR"}
    
    def detect_dbd_pattern(self, current_price: float, levels: Dict) -> Dict:
        """
        DBD: Support Break Down Retest
        Price breaks below support, pulls up, breaks again
        """
        
        support = levels["support"]
        
        # Price broke below support
        if current_price < support * 0.998:
            # Retest happening
            if self.prices[-2] > support and self.prices[-1] < support * 1.002:
                return {
                    "detected": True,
                    "pattern": "DBD",
                    "level": support,
                    "signal": "SHORT",
                    "entry": current_price,
                    "confidence": 85
                }
        
        return {"detected": False, "pattern": "DBD"}
    
    def detect_rbd_pattern(self, current_price: float, levels: Dict) -> Dict:
        """
        RBD: Resistance Break Down
        Price breaks above resistance then reverses down (trap)
        """
        
        resistance = levels["resistance"]
        
        # Price was above resistance, now falling
        if self.prices[-2] > resistance and current_price < resistance * 0.998:
            return {
                "detected": True,
                "pattern": "RBD",
                "level": resistance,
                "signal": "SHORT",
                "entry": current_price,
                "confidence": 75
            }
        
        return {"detected": False, "pattern": "RBD"}
    
    def detect_dbr_pattern(self, current_price: float, levels: Dict) -> Dict:
        """
        DBR: Support Break Up
        Price breaks below support then reverses up (trap)
        """
        
        support = levels["support"]
        
        # Price was below support, now rising
        if self.prices[-2] < support and current_price > support * 1.002:
            return {
                "detected": True,
                "pattern": "DBR",
                "level": support,
                "signal": "LONG",
                "entry": current_price,
                "confidence": 75
            }
        
        return {"detected": False, "pattern": "DBR"}
    
    def analyze(self, current_price: float) -> Dict:
        """Main 1H pattern analysis"""
        
        levels = self.find_resistance_support()
        
        rbr = self.detect_rbr_pattern(current_price, levels)
        dbd = self.detect_dbd_pattern(current_price, levels)
        rbd = self.detect_rbd_pattern(current_price, levels)
        dbr = self.detect_dbr_pattern(current_price, levels)
        
        # Get strongest pattern
        patterns = [rbr, dbd, rbd, dbr]
        detected = [p for p in patterns if p["detected"]]
        
        if detected:
            strongest = max(detected, key=lambda x: x.get("confidence", 0))
            signal = strongest["signal"]
        else:
            signal = "WAIT"
        
        result = {
            "levels": levels,
            "patterns": detected,
            "signal": signal,
            "strongest_pattern": detected[0]["pattern"] if detected else None
        }
        
        return result

