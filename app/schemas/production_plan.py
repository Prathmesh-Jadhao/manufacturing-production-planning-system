from datetime import date
from pydantic import BaseModel


class ProductionPlanResponse(BaseModel):
    plan_id: int
    plan_month: date
    product_id: str

    forecast_qty: int
    available_stock: int
    production_required: int

    capacity: int
    planned_quantity: int
    pending_quantity: int
    capacity_utilization: float

    status: str

    class Config:
        from_attributes = True