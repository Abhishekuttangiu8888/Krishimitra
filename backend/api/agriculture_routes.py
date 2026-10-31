
from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from pydantic import BaseModel, Field

from backend.integrations.mandi_prices import (
    get_mandi_filters,
    get_mandi_prices,
    MandiDataError,
)

from backend.integrations.gemini import (
    analyze_crop_disease,
    GeminiAPIError,
)

from backend.api.auth_routes import get_current_user
from backend.database.models import User


router = APIRouter(
    prefix="/agriculture",
    tags=["Agriculture"],
)

MAX_IMAGE_SIZE = 5 * 1024 * 1024


class MandiPriceRequest(BaseModel):
    district_id: int = Field(gt=0)
    market_id: int = Field(gt=0)
    commodity_id: int = Field(gt=0)
    selected_date: date


@router.get("/mandi/filters")
def mandi_filters(refresh: bool = False):
    try:
        data = get_mandi_filters(refresh=refresh)

        return {
            "success": True,
            "data": data,
        }

    except MandiDataError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )


@router.post("/mandi/prices")
def mandi_prices(request: MandiPriceRequest):
    try:
        result = get_mandi_prices(
            district_id=request.district_id,
            market_id=request.market_id,
            commodity_id=request.commodity_id,
            date=request.selected_date,
        )

        return {
            "success": True,
            "data": result,
        }

    except MandiDataError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve mandi prices.",
        )


def validate_image_signature(
    image_bytes: bytes,
    mime_type: str,
) -> bool:
    """Check that the uploaded file matches its declared image type."""

    if mime_type == "image/jpeg":
        return image_bytes.startswith(b"\xff\xd8\xff")

    if mime_type == "image/png":
        return image_bytes.startswith(b"\x89PNG\r\n\x1a\n")

    if mime_type == "image/webp":
        return (
            len(image_bytes) >= 12
            and image_bytes[:4] == b"RIFF"
            and image_bytes[8:12] == b"WEBP"
        )

    return False


@router.post("/disease/analyze")
def analyze_disease(
    image: UploadFile = File(...),
    crop_name: str = Form(...),
    symptoms: str = Form(""),
    affected_part: str = Form(""),
    duration: str = Form(""),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze a crop image using Gemini.

    Requires the farmer's authentication token.
    """

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Upload a JPG, PNG or WEBP image.",
        )

    if not crop_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide the crop name.",
        )

    try:
        image_bytes = image.file.read(MAX_IMAGE_SIZE + 1)

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded image is empty.",
            )

        if len(image_bytes) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Image size must not exceed 5 MB.",
            )

        if not validate_image_signature(
            image_bytes,
            image.content_type,
        ):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid supported image.",
            )

        profile = current_user.profile

        farmer_profile = None

        if profile:
            farmer_profile = {
                "state": profile.state,
                "district": profile.district,
                "taluk": profile.taluk,
                "village": profile.village,
                "preferred_language": profile.preferred_language,
                "crops": profile.crops,
            }

        result = analyze_crop_disease(
            image_bytes=image_bytes,
            mime_type=image.content_type,
            crop_name=crop_name.strip(),
            symptoms=symptoms.strip(),
            affected_part=affected_part.strip(),
            duration=duration.strip(),
            farmer_profile=farmer_profile,
        )

        return {
            "success": True,
            "message": "Crop image analysis completed.",
            "data": result,
        }

    except HTTPException:
        raise

    except GeminiAPIError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to analyze the crop image.",
        )

    finally:
        image.file.close()
