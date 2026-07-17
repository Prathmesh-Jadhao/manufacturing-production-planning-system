from pydantic import BaseModel


class MachineResponse(BaseModel):
    machine_id: str
    machine_name: str
    line_name: str
    daily_capacity: int
    shift_hours: int
    status: str

    class Config:
        from_attributes = True
