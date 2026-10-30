
import os
import base64

from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()


class SarvamTTSError(Exception):
    """Raised when Sarvam text-to-speech fails."""
    pass


def speak_text(text: str) -> bytes:
    """
    Convert Kannada text into female voice audio.

    Returns:
        WAV audio as bytes.
    """

    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise SarvamTTSError("Sarvam API key is missing.")

    if not text or not text.strip():
        raise SarvamTTSError("No text was provided.")

    if len(text) > 2500:
        raise SarvamTTSError("Text exceeds the 2500-character limit.")

    try:
        client = SarvamAI(
            api_subscription_key=api_key
        )

        response = client.text_to_speech.convert(
            text=text.strip(),
            model="bulbul:v4-flash",
            language_code="kn-IN",
            speaker="chaitra_kn_conversation",
            output_audio_codec="wav"
        )

        if not response.audios:
            raise SarvamTTSError("No audio was generated.")

        audio_bytes = base64.b64decode(response.audios[0])

        if not audio_bytes:
            raise SarvamTTSError("Generated audio is empty.")

        return audio_bytes

    except SarvamTTSError:
        raise

    except Exception as error:
        raise SarvamTTSError(
            f"Sarvam text-to-speech failed: {error}"
        ) from error
