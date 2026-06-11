from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.storage import save_report
import requests
import secrets

app = FastAPI()

API_KEY = "AIzaSyDl0NAsCQZ7Po-VLH_g4U0y1emnPsXXQY4"


@app.get("/")
def home():
    return {"message": "Trinetra API Running"}


@app.post("/webhook")
async def webhook(Body: str = Form(...)):

    # Generate report ID
    report_id = secrets.token_hex(4)

    # Save report
    save_report(report_id, Body)

    # Gemini API URL
    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    )

    # Prompt
    prompt = f"""
You are Trinetra AI, incident analysis assistant.

Analyze the report and provide:

Location:
Activity:
Risk Level:
Summary:

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
        summary = f"Report received. Analysis unavailable.\nError: {str(e)}"

    # WhatsApp Reply
    twilio_response = MessagingResponse()

    twilio_response.message(
        f"✅ Anonymous Report Received\n\n"
        f"Reference ID: {report_id}\n\n"
        f"{summary}"
    )

    return Response(
        content=str(twilio_response),
        media_type="application/xml"
    )