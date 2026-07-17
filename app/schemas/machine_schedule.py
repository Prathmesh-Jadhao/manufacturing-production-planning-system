from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class MachineScheduleResponse(BaseModel):
    schedule_id: int
    plan_id: int
    machine_id: str
    product_id: str
    scheduled_quantity: float
    utilization: float
    production_date: date
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
