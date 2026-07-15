from datetime import date
from pydantic import BaseModel


class MaterialRequirementResponse(BaseModel):
    requirement_id: int

    plan_id: int
    product_id: str
    material_id: str

    required_quantity: float
    available_stock: float
    shortage_quantity: float
    procurement_required: float

    procurement_status: str
    unit: str

    requirement_date: date
    status: str

    class Config:
        from_attributes = True