"""Algèbre humaine pour représentation qualitative."""

def qualitative_level(value: float) -> str:
    """Convertit une valeur [0,1] en symbole qualitatif."""
    if value >= 0.75:
        return "↑↑"
    elif value >= 0.55:
        return "↑"
    elif value >= 0.45:
        return "≈"
    elif value >= 0.25:
        return "↓"
    else:
        return "↓↓"

def features_summary(features: dict) -> str:
    """Résumé algébrique des features."""
    vol = features.get("volatility", 0.5)
    coh = features.get("coherence", 0.5)
    fric = features.get("friction", 0.5)
    regime = features.get("regime", "unknown")
    
    # Stabilité = inverse de volatilité
    stability = 1.0 - vol
    
    return f"S{qualitative_level(stability)}  C{qualitative_level(coh)}  F{qualitative_level(fric)}  | régime={regime}"

def gates_explainer(gates_result: dict) -> str:
    """Explication textuelle des gates."""
    decision = gates_result.get("decision", "UNKNOWN")
    reason = gates_result.get("reason", "")
    laws = gates_result.get("laws", [])
    
    laws_text = "\n".join([f"- {law}" for law in laws]) if laws else "—"
    
    return f"""Décision: {decision}
Raison: {reason}
Lois activées:
{laws_text}
"""
