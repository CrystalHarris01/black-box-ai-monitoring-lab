import json
from datetime import datetime

LOG_FILE = "logs/audit_log.json"

def write_log(prompt, response, results):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": response,
        "status": results["status"],
        "findings": results["findings"]
    }

    try:
        with open(LOG_FILE, "a") as file:
            file.write(json.dumps(entry) + "\n")

    except Exception as error:
        print(f"Logging error: {error}")
