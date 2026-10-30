
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

for attempt in range(3):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=(
                "ನಮಸ್ಕಾರ! ನೀವು KRISHI MITRA ಕೃಷಿ ಸಹಾಯಕರು. "
                "ಕರ್ನಾಟಕದ ರೈತನಿಗೆ ಕನ್ನಡದಲ್ಲಿ ಸ್ನೇಹಪೂರ್ವಕವಾಗಿ "
                "ನಮಸ್ಕಾರ ಹೇಳಿ."
            ),
        )

        print("\nGEMINI RESPONSE:\n")
        print(response.text)
        break

    except Exception as error:
        print(f"Attempt {attempt + 1} failed: {error}")

        if attempt < 2:
            time.sleep(2 ** (attempt + 1))
        else:
            print("\nGemini test failed after 3 attempts.")
