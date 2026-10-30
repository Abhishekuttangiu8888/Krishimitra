import jwt

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session, joinedload

from backend.database.connection import get_db
from backend.database.models import User, FarmerProfile

from backend.database.schemas import (
    SignupInput,
    LoginInput,
    TokenOutput,
    UserOutput,
)

from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in.",
        )

    try:
        user_id = decode_access_token(credentials.credentials)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid. Please log in.",
        )

    user = (
        db.query(User)
        .options(joinedload(User.profile))
        .filter(
            User.id == user_id,
            User.is_active.is_(True),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found or inactive.",
        )

    return user


@router.post(
    "/signup",
    response_model=TokenOutput,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    payload: SignupInput,
    db: Session = Depends(get_db),
):

    existing_user = (
        db.query(User)
        .filter(User.mobile == payload.mobile)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this mobile number already exists.",
        )

    user = User(
        mobile=payload.mobile,
        password_hash=hash_password(payload.password),
    )

    user.profile = FarmerProfile(
        **payload.profile.model_dump()
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Could not create account. Please try again.",
        )

    return TokenOutput(
        access_token=create_access_token(user.id),
        user=UserOutput.model_validate(user),
    )


@router.post("/login", response_model=TokenOutput)
def login(
    payload: LoginInput,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .options(joinedload(User.profile))
        .filter(User.mobile == payload.mobile)
        .first()
    )

    if (
        user is None
        or not verify_password(payload.password, user.password_hash)
        or not user.is_active
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect mobile number or password.",
        )

    return TokenOutput(
        access_token=create_access_token(user.id),
        user=UserOutput.model_validate(user),
    )


@router.get("/me", response_model=UserOutput)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return UserOutput.model_validate(current_user)