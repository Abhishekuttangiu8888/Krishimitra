from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import FarmerProfile, User
from backend.database.schemas import ProfileInput, ProfileOutput

from backend.api.auth_routes import get_current_user


router = APIRouter(
    prefix="/farmer",
    tags=["Farmer profile"],
)


@router.get("/profile", response_model=ProfileOutput)
def read_profile(
    current_user: User = Depends(get_current_user),
):

    if current_user.profile is None:
        raise HTTPException(
            status_code=404,
            detail="Farmer profile not found.",
        )

    return ProfileOutput.model_validate(current_user.profile)


@router.put("/profile", response_model=ProfileOutput)
def update_profile(
    payload: ProfileInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    profile = (
        db.query(FarmerProfile)
        .filter(FarmerProfile.user_id == current_user.id)
        .first()
    )

    if profile is None:

        profile = FarmerProfile(
            user_id=current_user.id,
            **payload.model_dump(),
        )

        db.add(profile)

    else:

        for key, value in payload.model_dump().items():
            setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return ProfileOutput.model_validate(profile)