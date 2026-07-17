from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductInventoryResponse(BaseModel):
    inventory_id: int
    product_id: str
    opening_stock: int
    current_stock: int
    safety_stock: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaterialInventoryResponse(BaseModel):
    material_id: str
    available_stock: float
    reorder_level: float
    location: str
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
