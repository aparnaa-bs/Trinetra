from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_report(text):

    prompt = f"""
    Extract:

    - Location
    - Activity
    - Risk Level

    Return JSON.

    Report:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text