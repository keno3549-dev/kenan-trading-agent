import numpy as np
from typing import List, Dict

class HarmonicPatternAnalyzer:
    """Harmonic Pattern Detection (Gartley, Bat, Crab, Cypher)"""
    
    def __init__(self, prices: List[float], lookback: int = 100):
        self.prices = np.array(prices[-lookback:])
        self.lookback = lookback
        self.tolerance = 0.05
    
    def find_abcd_points(self) -> List[tuple]:
        """Find potential A, B, C, D points from swing highs/lows"""
        points = []
        
        for i in range(5, len(self.prices) - 5):
            # High point
            if self.prices[i] == max(self.prices[i-5:i+6]):
                points.append((i, self.prices[i], "H"))
            # Low point
            elif self.prices[i] == min(self.prices[i-5:i+6]):
                points.append((i, self.prices[i], "L"))
        
        return points
    
    def is_ratio_valid(self, actual: float, expected: float) -> bool:
        """Check if ratio is within tolerance"""
        if expected == 0:
            return False
        deviation = abs(actual - expected) / expected
        return deviation <= self.tolerance
    
    def detect_gartley(self, points: List) -> Dict:
        """
        Gartley: AB=61.8% XA, BC=61.8% AB, CD=161.8% BC
        """
        if len(points) < 5:
            return {"detected": False}
        
        recent = points[-5:]
        X, A, B, C, D = recent[0][1], recent[1][1], recent[2][1], recent[3][1], recent[4][1]
        
        xa = abs(A - X)
        ab = abs(B - A) / xa if xa != 0 else 0
        bc = abs(C - B) / abs(B - A) if abs(B - A) != 0 else 0
        cd = abs(D - C) / abs(C - B) if abs(C - B) != 0 else 0
        
        is_gartley = (
            self.is_ratio_valid(ab, 0.618) and
            self.is_ratio_valid(bc, 0.618) and
            self.is_ratio_valid(cd, 1.618)
        )
        
        return {
            "detected": is_gartley,
            "pattern": "GARTLEY",
            "points": {"X": X, "A": A, "B": B, "C": C, "D": D},
            "direction": "BULLISH" if D < B else "BEARISH",
            "confidence": 90 if is_gartley else 0
        }
    
    def detect_bat(self, points: List) -> Dict:
        """
        Bat: AB=50% XA, BC=61.8% AB, CD=161.8% BC
        """
        if len(points) < 5:
            return {"detected": False}
        
        recent = points[-5:]
        X, A, B, C, D = recent[0][1], recent[1][1], recent[2][1], recent[3][1], recent[4][1]
        
        xa = abs(A - X)
        ab = abs(B - A) / xa if xa != 0 else 0
        bc = abs(C - B) / abs(B - A) if abs(B - A) != 0 else 0
        cd = abs(D - C) / abs(C - B) if abs(C - B) != 0 else 0
        
        is_bat = (
            self.is_ratio_valid(ab, 0.50) and
            self.is_ratio_valid(bc, 0.618) and
            self.is_ratio_valid(cd, 1.618)
        )
        
        return {
            "detected": is_bat,
            "pattern": "BAT",
            "points": {"X": X, "A": A, "B": B, "C": C, "D": D},
            "direction": "BULLISH" if D < B else "BEARISH",
            "confidence": 88 if is_bat else 0
        }
    
    def detect_crab(self, points: List) -> Dict:
        """
        Crab: AB=61.8% XA, BC=61.8% AB, CD=261.8% BC
        """
        if len(points) < 5:
            return {"detected": False}
        
        recent = points[-5:]
        X, A, B, C, D = recent[0][1], recent[1][1], recent[2][1], recent[3][1], recent[4][1]
        
        xa = abs(A - X)
        ab = abs(B - A) / xa if xa != 0 else 0
        bc = abs(C - B) / abs(B - A) if abs(B - A) != 0 else 0
        cd = abs(D - C) / abs(C - B) if abs(C - B) != 0 else 0
        
        is_crab = (
            self.is_ratio_valid(ab, 0.618) and
            self.is_ratio_valid(bc, 0.618) and
            self.is_ratio_valid(cd, 2.618)
        )
        
        return {
            "detected": is_crab,
            "pattern": "CRAB",
            "points": {"X": X, "A": A, "B": B, "C": C, "D": D},
            "direction": "BULLISH" if D < B else "BEARISH",
            "confidence": 92 if is_crab else 0
        }
    
    def detect_cypher(self, points: List) -> Dict:
        """
        Cypher: AB=61.8% XA, BC=127%-161.8% AB, CD=78.6% XA
        """
        if len(points) < 5:
            return {"detected": False}
        
        recent = points[-5:]
        X, A, B, C, D = recent[0][1], recent[1][1], recent[2][1], recent[3][1], recent[4][1]
        
        xa = abs(A - X)
        ab = abs(B - A) / xa if xa != 0 else 0
        bc = abs(C - B) / abs(B - A) if abs(B - A) != 0 else 0
        cd = abs(D - C) / xa if xa != 0 else 0
        
        is_cypher = (
            self.is_ratio_valid(ab, 0.618) and
            (self.is_ratio_valid(bc, 1.27) or self.is_ratio_valid(bc, 1.618)) and
            self.is_ratio_valid(cd, 0.786)
        )
        
        return {
            "detected": is_cypher,
            "pattern": "CYPHER",
            "points": {"X": X, "A": A, "B": B, "C": C, "D": D},
            "direction": "BULLISH" if D < B else "BEARISH",
            "confidence": 85 if is_cypher else 0
        }
    
    def analyze(self) -> Dict:
        """Main harmonic analysis"""
        points = self.find_abcd_points()
        
        patterns = [
            self.detect_gartley(points),
            self.detect_bat(points),
            self.detect_crab(points),
            self.detect_cypher(points)
        ]
        
        detected = [p for p in patterns if p["detected"]]
        
        result = {
            "patterns_detected": len(detected),
            "patterns": detected,
            "signal": self._generate_signal(detected)
        }
        
        return result
    
    def _generate_signal(self, patterns: List) -> str:
        """Generate signal from patterns"""
        if not patterns:
            return "WAIT"
        
        bullish = sum(1 for p in patterns if p["direction"] == "BULLISH")
        bearish = sum(1 for p in patterns if p["direction"] == "BEARISH")
        
        if bullish > bearish:
            return "LONG"
        elif bearish > bullish:
            return "SHORT"
        else:
            return "WAIT"

