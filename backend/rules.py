import json
import os
from typing import List, Dict, Any
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

FINES_CONFIG = config.get("FINES", {})

def calculate_fine(violation_type: str, challan_history: List[Dict[str, Any]], detection_date_iso: str) -> Dict[str, Any]:
    """
    Pure, config-driven function mapping (violation_type, plate_history) -> {amount, escalation_applied}
    """
    rule = FINES_CONFIG.get(violation_type)
    if not rule:
        # Fallback for unknown violations
        return {"amount": 0, "escalation_applied": False, "flags": []}

    base_fine = rule["base_fine"]
    escalation_amount = rule["escalation_amount"]
    escalation_threshold_days = rule["escalation_threshold_days"]
    flags = rule["flags"]

    if escalation_amount == 0 or escalation_threshold_days == 0:
        return {"amount": base_fine, "escalation_applied": False, "flags": flags}

    try:
        detection_date = datetime.fromisoformat(detection_date_iso.replace('Z', '+00:00'))
    except ValueError:
        detection_date = datetime.now()

    # Check for repeat offense within the threshold window
    escalation_applied = False
    for past_challan in challan_history:
        if past_challan.get("type") == violation_type:
            past_date_str = past_challan.get("detected_at", "")
            try:
                past_date = datetime.fromisoformat(past_date_str.replace('Z', '+00:00'))
                days_diff = (detection_date - past_date).days
                if 0 <= days_diff <= escalation_threshold_days:
                    escalation_applied = True
                    break
            except Exception:
                continue

    final_amount = escalation_amount if escalation_applied else base_fine

    return {
        "amount": final_amount,
        "escalation_applied": escalation_applied,
        "flags": flags
    }
