from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class TradeIntentERC8004:
    # Minimal, hackathon-safe intent representation
    standard: str
    version: str
    asset: str
    side: str      # BUY/SELL
    amount: float
    timestamp: float
    metadata: Dict[str, Any]

def build_trade_intent(asset: str, side: str, amount: float, timestamp: float, metadata: dict) -> dict:
    intent = TradeIntentERC8004(
        standard="ERC-8004",
        version="0.1",
        asset=asset,
        side=side,
        amount=float(amount),
        timestamp=float(timestamp),
        metadata=dict(metadata or {}),
    )
    return asdict(intent)
