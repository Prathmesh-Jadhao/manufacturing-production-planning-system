from pydantic import BaseModel


class MaterialResponse(BaseModel):
    material_id: str
    material_name: str
    unit: str

    class Config:
        from_attributes = True