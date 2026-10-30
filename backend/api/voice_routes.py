
from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.integrations.sarvam import (
    transcribe_audio,
    SarvamAPIError
)

router = APIRouter(prefix="/voice", tags=["Voice"])

MAX_AUDIO_SIZE = 15 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".wav", ".mp3", ".m4a", ".ogg", ".flac", ".webm"
}


@router.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):

    filename = audio.filename or "recording.wav"

    extension = "." + filename.rsplit(".", 1)[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    audio_bytes = await audio.read(MAX_AUDIO_SIZE + 1)

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="No audio was provided."
        )

    if len(audio_bytes) > MAX_AUDIO_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Audio file is too large. Maximum size is 15 MB."
        )

    try:
        result = transcribe_audio(
            audio_bytes=audio_bytes,
            filename=filename
        )

        return {
            "success": True,
            "provider": "Sarvam AI",
            "text": result["text"]
        }

    except SarvamAPIError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )
