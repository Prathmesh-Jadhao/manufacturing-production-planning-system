from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class ForecastResponse(BaseModel):
    forecast_id: int
    forecast_month: date
    product_id: str
    forecast_qty: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
