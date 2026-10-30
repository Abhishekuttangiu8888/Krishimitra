from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.integrations.mandi_prices import (
    get_mandi_filters,
    get_mandi_prices,
    MandiDataError,
)


router = APIRouter(
    prefix="/agriculture",
    tags=["Agriculture"],
)


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