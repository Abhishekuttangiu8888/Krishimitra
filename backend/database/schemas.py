
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class ProfileInput(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)

    preferred_language: str = Field(
        default="kn",
        pattern="^(kn|en)$",
    )

    state: str = Field(default="Karnataka", max_length=80)
    district: Optional[str] = Field(default=None, max_length=100)
    taluk: Optional[str] = Field(default=None, max_length=100)
    village: Optional[str] = Field(default=None, max_length=120)

    land_area: Optional[str] = Field(default=None, max_length=40)
    land_unit: str = Field(default="acres", max_length=30)
    land_ownership: Optional[str] = Field(default=None, max_length=40)

    crops: list[str] = Field(default_factory=list, max_length=20)

    irrigation_method: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    farming_type: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    needs: list[str] = Field(default_factory=list, max_length=30)

    @field_validator("full_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = " ".join(value.split())

        if len(value) < 2:
            raise ValueError("Please enter your full name.")

        return value


class SignupInput(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=8, max_length=128)
    profile: ProfileInput

    @field_validator("mobile")
    @classmethod
    def clean_mobile(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())

        if not 10 <= len(digits) <= 15:
            raise ValueError("Enter a valid mobile number.")

        return digits


class LoginInput(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("mobile")
    @classmethod
    def clean_mobile(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())

        if not 10 <= len(digits) <= 15:
            raise ValueError("Enter a valid mobile number.")

        return digits


class ProfileOutput(ProfileInput):
    model_config = ConfigDict(from_attributes=True)


class UserOutput(BaseModel):
    id: int
    mobile: str
    profile: ProfileOutput | None = None

    model_config = ConfigDict(from_attributes=True)


class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOutput
