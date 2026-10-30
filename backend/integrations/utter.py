
import os
import requests
from dotenv import load_dotenv

load_dotenv()

UTTER_API_URL = "https://api.utter.cc/v1/transcribe"


class UtterAPIError(Exception):
    """Raised when Utter speech recognition fails."""
    pass


def transcribe_audio(
    audio_bytes: bytes,
    filename: str = "recording.wav",
    language: str | None = None,
) -> dict:
    """
    Convert an audio recording into text using Utter.

    Args:
        audio_bytes: Recorded audio file as bytes.
        filename: Original audio filename.
        language: Optional language code.
                  Leave None for automatic language detection.

    Returns:
        Dictionary containing recognized text and metadata.
    """

    api_key = os.getenv("UTTER_API_KEY")

    if not api_key:
        raise UtterAPIError("Utter API key is missing.")

    if not audio_bytes:
        raise UtterAPIError("No audio was provided.")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    files = {
        "file": (
            filename,
            audio_bytes,
            "application/octet-stream"
        )
    }

    data = {
        "tier": "standard"
    }

    # Automatic language detection if language is not specified.
    if language:
        data["language"] = language

    try:
        response = requests.post(
            UTTER_API_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=300
        )

        if response.status_code != 200:
            try:
                error_data = response.json().get("error", {})
                error_message = error_data.get(
                    "message",
                    "Speech recognition request failed."
                )
            except ValueError:
                error_message = "Utter returned an unexpected response."

            raise UtterAPIError(
                f"Utter API error ({response.status_code}): "
                f"{error_message}"
            )

        result = response.json()

        recognized_text = result.get("text", "").strip()

        if not recognized_text:
            raise UtterAPIError(
                "No speech was recognized. Please try again."
            )

        return {
            "text": recognized_text,
            "languages": result.get("languages", []),
            "audio_seconds": result.get("audio_seconds"),
            "request_id": result.get("request_id")
        }

    except requests.Timeout:
        raise UtterAPIError(
            "Speech recognition timed out. Please try again."
        )

    except requests.RequestException:
        raise UtterAPIError(
            "Could not connect to Utter. Check your internet connection."
        )
