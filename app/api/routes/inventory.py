from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import Inventory
from app.models.material_inventory import MaterialInventory
from app.schemas.inventory import ProductInventoryResponse, MaterialInventoryResponse

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get("/product", response_model=list[ProductInventoryResponse])
def get_product_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@router.get("/material", response_model=list[MaterialInventoryResponse])
def get_material_inventory(db: Session = Depends(get_db)):
    return db.query(MaterialInventory).all()
