import numpy as np
from typing import List, Dict
from datetime import datetime

class SignalGenerator:
    """Generate trading signals from all analyzers"""
    
    def __init__(self, min_confidence: int = 90):
        self.min_confidence = min_confidence
    
    def generate_signal(self, 
                       symbol: str,
                       market_structure: Dict,
                       multi_timeframe: Dict,
                       harmonic: Dict,
                       price_action: Dict,
                       current_price: float,
                       volume: Dict) -> Dict:
        """
        Generate final signal with strict rules:
        - Only 90%+ confidence
        - ALL conditions must be FORMED (not predicted)
        - Harmonic > 4H MS > 1H patterns > Price action
        """
        
        # TIER SCORING SYSTEM
        tier_score = self._calculate_tier_score(
            market_structure, 
            multi_timeframe, 
            harmonic, 
            price_action, 
            volume
        )
        
        # Strict rule: 90%+ confidence only
        if tier_score["score"] < self.min_confidence:
            return {
                "symbol": symbol,
                "signal": "WAIT",
                "reason": f"Confidence too low ({tier_score['score']}%)",
                "confidence": tier_score["score"],
                "tier": "REJECTED",
                "timestamp": datetime.now().isoformat()
            }
        
        # Generate entry/exit points
        entry = self._calculate_entry(
            current_price, 
            market_structure, 
            multi_timeframe, 
            price_action
        )
        
        targets = self._calculate_targets(
            entry, 
            market_structure, 
            harmonic, 
            price_action
        )
        
        stop_loss = self._calculate_stop_loss(
            entry, 
            market_structure, 
            price_action
        )
        
        # Risk/Reward validation
        risk_reward = self._validate_risk_reward(entry, targets, stop_loss)
        
        if not risk_reward["valid"]:
            return {
                "symbol": symbol,
                "signal": "WAIT",
                "reason": f"Risk/Reward < 1:2 ({risk_reward['ratio']:.2f})",
                "confidence": tier_score["score"],
                "tier": "REJECTED",
                "timestamp": datetime.now().isoformat()
            }
        
        # Final signal
        final_signal = tier_score["signal"]
        
        return {
            "symbol": symbol,
            "signal": final_signal,
            "confidence": tier_score["score"],
            "tier": tier_score["tier"],
            "entry": entry,
            "tp1": targets["tp1"],
            "tp2": targets["tp2"],
            "tp3": targets["tp3"],
            "sl": stop_loss,
            "risk_reward": risk_reward["ratio"],
            "confluence": tier_score["confluence"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_tier_score(self, ms: Dict, mtf: Dict, harmonic: Dict, pa: Dict, vol: Dict) -> Dict:
        """
        TIER 1 (95%+): Harmonic D + 4H MS Break + 1H pattern + Volume
        TIER 2 (85-90%): 4H MS Break + 1H pattern + Volume
        TIER 3 (75-80%): Breaker block + QML + Volume
        TIER 4 (<75%): Single pattern (REJECT)
        """
        
        score = 0
        confluence = []
        
        # HARMONIC: +40 points (highest priority)
        if harmonic.get("patterns_detected", 0) > 0:
            score += 40
            confluence.append("Harmonic Pattern")
        
        # 4H MARKET STRUCTURE BREAK: +30 points
        if ms.get("bos", {}).get("bos"):
            score += 30
            confluence.append("4H BOS")
        
        # 1H PATTERNS (RBR/DBD): +20 points
        if mtf.get("patterns") and len(mtf["patterns"]) > 0:
            score += 20
            confluence.append(f"1H {mtf.get('strongest_pattern')}")
        
        # VOLUME SPIKE: +10 points
        if vol.get("has_spike"):
            score += 10
            confluence.append("Volume Spike")
        
        # Determine tier and signal
        if score >= 95:
            tier = "TIER_1"
            signal = self._determine_signal(harmonic, ms, mtf)
        elif score >= 85:
            tier = "TIER_2"
            signal = self._determine_signal(ms, mtf, pa)
        elif score >= 75:
            tier = "TIER_3"
            signal = self._determine_signal(pa)
        else:
            tier = "TIER_4"
            signal = "WAIT"
        
        return {
            "score": score,
            "tier": tier,
            "signal": signal,
            "confluence": confluence
        }
    
    def _determine_signal(self, *analyzers) -> str:
        """Determine LONG/SHORT/WAIT from analyzers"""
        
        signals = []
        for analyzer in analyzers:
            if analyzer and analyzer.get("signal"):
                signals.append(analyzer["signal"])
        
        if not signals:
            return "WAIT"
        
        long_count = signals.count("LONG")
        short_count = signals.count("SHORT")
        
        if long_count > short_count:
            return "LONG"
        elif short_count > long_count:
            return "SHORT"
        else:
            return "WAIT"
    
    def _calculate_entry(self, current_price: float, ms: Dict, mtf: Dict, pa: Dict) -> float:
        """Calculate entry price"""
        
        # 1H pattern retest zone
        if mtf.get("patterns") and len(mtf["patterns"]) > 0:
            return mtf["patterns"][0].get("entry", current_price)
        
        # Breaker block zone
        breakers = pa.get("breaker_blocks", [])
        if breakers:
            return breakers[0].get("entry_zone", (current_price, current_price))[0]
        
        # Default: current price
        return current_price
    
    def _calculate_targets(self, entry: float, ms: Dict, harmonic: Dict, pa: Dict) -> Dict:
        """Calculate TP1, TP2, TP3"""
        
        # Use order blocks or harmonic targets
        orders = pa.get("order_blocks", [])
        qml = pa.get("qml", {})
        
        # Estimate range (order block high/low)
        if orders:
            range_size = abs(orders[0]["high"] - orders[0]["low"])
        else:
            range_size = abs(entry - qml.get("qml_low", entry)) if entry > qml.get("qml", entry) else abs(entry - qml.get("qml_high", entry))
        
        if entry > qml.get("qml", entry):  # Bullish
            tp1 = entry + range_size * 0.5
            tp2 = entry + range_size * 1.0
            tp3 = entry + range_size * 1.5
        else:  # Bearish
            tp1 = entry - range_size * 0.5
            tp2 = entry - range_size * 1.0
            tp3 = entry - range_size * 1.5
        
        return {"tp1": tp1, "tp2": tp2, "tp3": tp3}
    
    def _calculate_stop_loss(self, entry: float, ms: Dict, pa: Dict) -> float:
        """Calculate SL from breaker blocks or order blocks"""
        
        orders = pa.get("order_blocks", [])
        breakers = pa.get("breaker_blocks", [])
        
        if orders:
            return orders[0]["low"] if entry > orders[0]["high"] else orders[0]["high"]
        
        if breakers:
            return breakers[0]["level"]
        
        # Default: entry - 2%
        return entry * 0.98 if entry > pa.get("qml", {}).get("qml") else entry * 1.02
    
    def _validate_risk_reward(self, entry: float, targets: Dict, sl: float) -> Dict:
        """Validate risk/reward ratio (min 1:2)"""
        
        risk = abs(entry - sl)
        reward = abs(targets["tp2"] - entry)
        
        ratio = reward / risk if risk > 0 else 0
        valid = ratio >= 2.0
        
        return {
            "ratio": ratio,
            "valid": valid
        }

