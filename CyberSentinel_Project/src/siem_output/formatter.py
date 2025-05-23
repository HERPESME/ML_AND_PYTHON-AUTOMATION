import json
from datetime import datetime


def format_for_siem(alert, fmt="json"):
    alert["timestamp"] = datetime.utcnow().isoformat()

    if fmt == "json":
        return json.dumps(alert)
    elif fmt == "text":
        return "\n".join(f"{k}: {v}" for k, v in alert.items())
    else:
        raise ValueError("Unsupported SIEM format: choose 'json' or 'text'")
