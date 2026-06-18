from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.storage import save_report, save_media
import requests
import secrets
import dotenv

app = FastAPI()
load_dotenv()
API_KEY = "GEMINI_API_KEY"

# Stores latest report ID for each WhatsApp user
pending_reports = {}


@app.get("/")
def home():
    return {"message": "Trinetra API Running"}


@app.post("/webhook")
async def webhook(
    From: str = Form(""),
    Body: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None)
):

    print("WHATSAPP MESSAGE RECEIVED:", Body)

    user_message = Body.strip().upper()

    # ==========================
    # USER REPLIES YES
    # ==========================
    if user_message == "YES":

        report_id = pending_reports.get(From, "UNKNOWN")

        resp = MessagingResponse()

        resp.message(
            f"""Thank you.

Please send any photos related to this report.

Your evidence will be securely attached to Report ID: {report_id} and can be reviewed later by authorized personnel.

⚠️ Your safety comes first.

Do not put yourself at risk to collect evidence."""
        )

        return Response(
            content=str(resp),
            media_type="application/xml"
        )

    # ==========================
    # USER REPLIES NO
    # ==========================
    if user_message == "NO":

        resp = MessagingResponse()

        resp.message(
            """Okay, thank you for informing us.

Your report has been securely recorded and forwarded for review.

We appreciate your cooperation and willingness to help keep the community safe.

Take care and stay safe."""
        )

        return Response(
            content=str(resp),
            media_type="application/xml"
        )

    # ==========================
    # USER SENDS MEDIA
    # ==========================
    if NumMedia > 0:

        report_id = pending_reports.get(From, "UNKNOWN")

        save_media(
            report_id,
            MediaUrl0,
            MediaContentType0
        )

        resp = MessagingResponse()

        resp.message(
            f"""✅ Evidence Received

Reference ID: {report_id}

Your image/video has been securely attached to the report.

Thank you for assisting the investigation.

Please stay safe."""
        )

        return Response(
            content=str(resp),
            media_type="application/xml"
        )

    # ==========================
    # NEW REPORT
    # ==========================
    report_id = "TRN-" + secrets.token_hex(4).upper()

    pending_reports[From] = report_id

    save_report(report_id, Body)

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    )

    prompt = f"""
You are Trinetra AI, a campus safety assistant.

Analyze the report and return ONLY in this format:

Location: <location>
Activity: <activity>
Risk Level: <Low/Medium/High>
Summary: <short summary>

Report:
{Body}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(url, json=payload)
        data = response.json()

        summary = data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:

        print("Gemini Error:", e)

        summary = """
Location: Unknown
Activity: Unable to analyze
Risk Level: Unknown
Summary: Report received successfully.
"""

    resp = MessagingResponse()

    resp.message(
        f"""✅ Anonymous Report Received

Reference ID: {report_id}

Thank you for reporting this incident.

{summary}

Your report has been securely recorded.

📷 Do you have any supporting images or videos related to this incident?

Reply:
YES - to upload evidence
NO - if you do not have any evidence

Please stay safe and avoid confronting anyone involved.

⚠️ Do not put yourself in danger to collect evidence.

You have done a responsible thing by reporting this. Your information may help protect others and support appropriate action by authorities."""
    )

    return Response(
        content=str(resp),
        media_type="application/xml"
    )
