import json
from datetime import datetime

def save_report(report_id, message):
    report = {
        "report_id": report_id,
        "message": message,
        "timestamp": str(datetime.now())
    }

    try:
        with open("reports.json", "r") as f:
            reports = json.load(f)
    except:
        reports = []

    reports.append(report)

    with open("reports.json", "w") as f:
        json.dump(reports, f, indent=4)