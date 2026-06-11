# Trinetra

Trinetra is an AI-powered anonymous incident reporting system that enables citizens or students to report suspicious activities through WhatsApp.

## Features

- Anonymous reporting through WhatsApp
- AI-powered incident analysis using Gemini
- Risk level assessment
- Evidence collection (images/videos)
- Secure report storage
- Unique report tracking IDs
- Automated acknowledgement and guidance

## Tech Stack

- FastAPI
- Twilio WhatsApp Sandbox
- Google Gemini API
- Python
- JSON Storage

## Project Workflow

1. User sends a report through WhatsApp.
2. Trinetra generates a unique report ID.
3. Gemini analyzes the report.
4. Location, activity and risk level are extracted.
5. User receives an AI-generated response.
6. User may optionally upload supporting images/videos.
7. Evidence is linked to the report for later review.

## Installation

```bash
git clone <repository-url>

cd trinetra

pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

## Configure Twilio

1. Create a Twilio account.
2. Enable WhatsApp Sandbox.
3. Configure:

```
https://<ngrok-url>/webhook
```

as the webhook URL.

## Configure Gemini

Add your Gemini API key:

```python
API_KEY = "YOUR_GEMINI_API_KEY"
```

## Example Report

```
A group is selling drugs near the college bus stop.
```

Example Response:

```
Location: College Bus Stop
Activity: Suspected Drug Distribution
Risk Level: High
Summary: Illegal substances are reportedly being sold near a public area.
```

## Future Enhancements

- Admin dashboard
- Database integration
- Real-time alerts
- GIS mapping
- Police portal
- Evidence management system

## Team

Team Trinetra

Built for Hackathon 2026
