
import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

if not api_key:
    print("ERROR: Sarvam API key not found.")
    raise SystemExit(1)

audio_path = "kannada_test.wav.m4a"

if not os.path.exists(audio_path):
    print("ERROR: Audio file not found:", audio_path)
    raise SystemExit(1)

print("Connecting to Sarvam AI...")

try:
    client = SarvamAI(api_subscription_key=api_key)

    with open(audio_path, "rb") as audio:
        response = client.speech_to_text.transcribe(
            file=audio,
            model="saaras:v4",
            mode="transcribe"
        )

    print("\nSUCCESS!")
    print("Recognized Kannada text:")
    print(response.transcript)

except Exception as error:
    print("\nSarvam API error:")
    print(str(error))
