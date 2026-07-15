from datetime import datetime
from pydantic import BaseModel


class ProductInventoryResponse(BaseModel):
    inventory_id: int
    product_id: str
    opening_stock: int
    current_stock: int
    safety_stock: int
    last_updated: datetime

    class Config:
        from_attributes = True


class MaterialInventoryResponse(BaseModel):
    material_id: str
    available_stock: float
    reorder_level: float
    location: str

    class Config:
        from_attributes = True
