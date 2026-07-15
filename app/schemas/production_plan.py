from datetime import date
from pydantic import BaseModel


class ProductionPlanResponse(BaseModel):
    plan_id: int
    plan_month: date
    product_id: str

    forecast_qty: float
    available_stock: float
    production_required: float

    capacity: float
    planned_quantity: float
    pending_quantity: float
    capacity_utilization: float

    status: str

    class Config:
        from_attributes = True