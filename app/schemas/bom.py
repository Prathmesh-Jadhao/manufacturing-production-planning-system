from datetime import date
from typing import Optional

from pydantic import BaseModel


class BOMResponse(BaseModel):
    bom_id: int
    product_id: str
    material_id: str
    quantity_per_unit: float
    scrap_percentage: float
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None

    class Config:
        from_attributes = True
