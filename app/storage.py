import json
from datetime import datetime

FILE_NAME = "reports.json"


def load_reports():

    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)

    except:
        return []


def save_reports(reports):

    with open(FILE_NAME, "w") as f:
        json.dump(reports, f, indent=4)


def save_report(report_id, message):

    reports = load_reports()

    reports.append({
        "report_id": report_id,
        "message": message,
        "timestamp": str(datetime.now()),
        "evidence": []
    })

    save_reports(reports)


def save_media(report_id, media_url, media_type):

    reports = load_reports()

    reports.append({
        "report_id": report_id,
        "message": "Media Evidence",
        "timestamp": str(datetime.now()),
        "evidence": [
            {
                "type": media_type,
                "url": media_url
            }
        ]
    })

    save_reports(reports)