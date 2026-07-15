from pydantic import BaseModel


class ProductResponse(BaseModel):
    product_id: str
    product_name: str
    family: str
    size_mm: int
    unit: str
    status: str

    class Config:
        from_attributes = True