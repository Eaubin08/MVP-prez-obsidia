from typing import Tuple, Dict, Any

def execute_dry(intent: dict) -> Tuple[bool, Dict[str, Any]]:
    # No broker. Returns a fake order id and status.
    return True, {"order_id": f"dry-{int(intent['timestamp']*1000)}", "status": "FILLED"}
