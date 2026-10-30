
import os
from io import BytesIO

from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()


class SarvamAPIError(Exception):
    """Raised when Sarvam speech recognition fails."""
    pass


def transcribe_audio(
    audio_bytes: bytes,
    filename: str = "recording.wav"
) -> dict:

    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise SarvamAPIError("Sarvam API key is missing.")

    if not audio_bytes:
        raise SarvamAPIError("No audio was provided.")

    try:
        client = SarvamAI(api_subscription_key=api_key)

        audio_file = BytesIO(audio_bytes)
        audio_file.name = filename

        response = client.speech_to_text.transcribe(
            file=audio_file,
            model="saaras:v4",
            mode="transcribe"
        )

        recognized_text = response.transcript.strip()

        if not recognized_text:
            raise SarvamAPIError(
                "No speech was recognized. Please try again."
            )

        return {
            "text": recognized_text
        }

    except SarvamAPIError:
        raise

    except Exception as error:
        raise SarvamAPIError(
            f"Sarvam transcription failed: {error}"
        ) from error
