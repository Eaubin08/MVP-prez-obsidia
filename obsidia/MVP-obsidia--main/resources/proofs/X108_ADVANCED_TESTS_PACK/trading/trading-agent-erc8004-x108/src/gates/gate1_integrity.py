REQUIRED_FIELDS = ("asset", "side", "amount", "timestamp", "coherence")

def gate1_validate_intent(intent: dict):
    missing = [k for k in REQUIRED_FIELDS if k not in intent]
    if missing:
        return False, "invalid_intent_missing_fields:" + ",".join(missing)
    # basic checks
    if intent["side"] not in ("BUY", "SELL"):
        return False, "invalid_intent_side"
    if float(intent["amount"]) <= 0:
        return False, "invalid_intent_amount"
    if not (0.0 <= float(intent["coherence"]) <= 1.0):
        return False, "invalid_intent_coherence"
    return True, "pass"
