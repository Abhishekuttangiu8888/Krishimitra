
import os
import requests
import mimetypes
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("UTTER_API_KEY")

if not api_key:
    print("ERROR: API key not found")
    raise SystemExit(1)

audio_path = "kannada_test.wav.m4a"

if not os.path.exists(audio_path):
    print("ERROR: Audio file not found:", audio_path)
    raise SystemExit(1)

mime_type = mimetypes.guess_type(audio_path)[0] or "audio/mp4"

print("Sending audio to Utter...")
print("Audio format:", mime_type)
print("File size:", os.path.getsize(audio_path), "bytes")

try:
    with open(audio_path, "rb") as audio:
        response = requests.post(
            "https://api.utter.cc/v1/transcribe",
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            files={
                "file": (
                    "kannada_test.m4a",
                    audio,
                    mime_type
                )
            },
            data={
                "tier": "standard"
            },
            timeout=300
        )

    print("\nHTTP Status:", response.status_code)

    try:
        result = response.json()
        print("Response:", result)

        if response.status_code == 200:
            print("\nRECOGNIZED TEXT:")
            print(result.get("text"))

    except ValueError:
        print("Response:", response.text)

except requests.RequestException as error:
    print("Connection error:", error)
