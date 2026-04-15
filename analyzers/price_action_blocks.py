import numpy as np
from typing import List, Dict

class PriceActionAnalyzer:
    """Price Action Analysis (QML, Breaker Blocks, Order Blocks)"""
    
    def __init__(self, prices: List[float], volumes: List[float] = None, lookback: int = 100):
        self.prices = np.array(prices[-lookback:])
        self.volumes = np.array(volumes[-lookback:]) if volumes else np.ones(lookback)
        self.lookback = lookback
    
    # ============ QML (Quantitative Mean Level) ============
    
    def calculate_qml(self, window: int = 20) -> Dict:
        """
        QML: (20-bar High + 20-bar Low) / 2
        Bullish if price > QML, Bearish if price < QML
        """
        
        recent = self.prices[-window:]
        qml_high = max(recent)
        qml_low = min(recent)
        qml = (qml_high + qml_low) / 2
        
        current_price = self.prices[-1]
        
        if current_price > qml:
            bias = "BULLISH"
        elif current_price < qml:
            bias = "BEARISH"
        else:
            bias = "NEUTRAL"
        
        return {
            "qml": qml,
            "qml_high": qml_high,
            "qml_low": qml_low,
            "current_price": current_price,
            "distance": current_price - qml,
            "bias": bias
        }
    
    # ============ BREAKER BLOCKS ============
    
    def detect_breaker_blocks(self, window: int = 20) -> List[Dict]:
        """
        Breaker Block: Old resistance/support that price breaks
        Retest of breaker = Strong entry point
        """
        
        blocks = []
        recent = self.prices[-window:]
        
        resistance = max(recent)
        support = min(recent)
        
        current_price = self.prices[-1]
        
        # Bullish Breaker: Price broke below old support, now retesting
        if current_price > support and self.prices[-2] < support:
            blocks.append({
                "type": "BULLISH_BREAKER",
                "level": support,
                "description": "Price broke support, now retesting",
                "signal": "LONG",
                "entry_zone": (support, support * 1.002)
            })
        
        # Bearish Breaker: Price broke above old resistance, now retesting
        if current_price < resistance and self.prices[-2] > resistance:
            blocks.append({
                "type": "BEARISH_BREAKER",
                "level": resistance,
                "description": "Price broke resistance, now retesting",
                "signal": "SHORT",
                "entry_zone": (resistance * 0.998, resistance)
            })
        
        return blocks
    
    # ============ ORDER BLOCKS (Liquidity Pools) ============
    
    def detect_order_blocks(self, lookback_bars: int = 20) -> List[Dict]:
        """
        Order Block: Strong candle's high/low where liquidity pools
        Price retest = Strong entry
        """
        
        blocks = []
        recent = self.prices[-lookback_bars:]
        
        for i in range(1, len(recent) - 2):
            # Strong up candle (order block)
            if recent[i] > recent[i-1]:
                candle_high = recent[i]
                candle_low = recent[i-1]
                
                # Price broke below and may retest
                if recent[i+1] < candle_low:
                    blocks.append({
                        "type": "BULLISH_OB",
                        "high": candle_high,
                        "low": candle_low,
                        "index": i,
                        "signal": "LONG",
                        "description": "Bullish OB - expect bounce"
                    })
            
            # Strong down candle (order block)
            elif recent[i] < recent[i-1]:
                candle_high = recent[i-1]
                candle_low = recent[i]
                
                # Price broke above and may retest
                if recent[i+1] > candle_high:
                    blocks.append({
                        "type": "BEARISH_OB",
                        "high": candle_high,
                        "low": candle_low,
                        "index": i,
                        "signal": "SHORT",
                        "description": "Bearish OB - expect rejection"
                    })
        
        return blocks
    
    # ============ VOLUME CONFIRMATION ============
    
    def check_volume_spike(self, threshold: float = 2.0) -> Dict:
        """
        Volume Spike: Current volume > threshold * average volume
        Institutional activity confirmation
        """
        
        avg_volume = np.mean(self.volumes)
        current_volume = self.volumes[-1]
        spike_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        has_spike = spike_ratio > threshold
        
        return {
            "current_volume": current_volume,
            "average_volume": avg_volume,
            "spike_ratio": spike_ratio,
            "has_spike": has_spike,
            "confirmation": "STRONG" if has_spike else "WEAK"
        }
    
    # ============ MAIN ANALYSIS ============
    
    def analyze(self, current_price: float = None) -> Dict:
        """Main price action analysis"""
        
        if current_price is None:
            current_price = self.prices[-1]
        
        qml = self.calculate_qml()
        breakers = self.detect_breaker_blocks()
        orders = self.detect_order_blocks()
        volume = self.check_volume_spike()
        
        # Generate signal
        signal = self._generate_signal(qml, breakers, orders)
        
        result = {
            "qml": qml,
            "breaker_blocks": breakers,
            "order_blocks": orders,
            "volume": volume,
            "signal": signal,
            "confluence_score": self._calculate_confluence(qml, breakers, orders, volume)
        }
        
        return result
    
    def _generate_signal(self, qml: Dict, breakers: List, orders: List) -> str:
        """Generate signal from price action"""
        
        signals = []
        
        # QML bias
        if qml["bias"] == "BULLISH":
            signals.append("LONG")
        elif qml["bias"] == "BEARISH":
            signals.append("SHORT")
        
        # Breaker blocks
        for block in breakers:
            signals.append(block["signal"])
        
        # Order blocks
        for block in orders:
            signals.append(block["signal"])
        
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
    
    def _calculate_confluence(self, qml: Dict, breakers: List, orders: List, volume: Dict) -> int:
        """Calculate confluence score (0-100)"""
        
        score = 0
        
        # QML alignment: +25
        if qml["bias"] != "NEUTRAL":
            score += 25
        
        # Breaker blocks: +25
        if breakers:
            score += 25
        
        # Order blocks: +25
        if orders:
            score += 25
        
        # Volume confirmation: +25
        if volume["has_spike"]:
            score += 25
        
        return min(score, 100)

