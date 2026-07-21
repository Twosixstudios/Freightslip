import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema import RateConfirmation

load_dotenv()

def parse_rate_con_pdf(pdf_bytes: bytes) -> RateConfirmation:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY missing in .env")

    client = genai.Client(api_key=api_key, vertexai=False)

    # Pass raw PDF bytes directly into Gemini's vision engine
    pdf_part = types.Part.from_bytes(
        data=pdf_bytes,
        mime_type="application/pdf"
    )

    prompt = "Extract structured load details and financial figures from this rate confirmation document."

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=[pdf_part, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RateConfirmation,
            temperature=0.1,
        ),
    )

    return RateConfirmation.model_validate_json(response.text)