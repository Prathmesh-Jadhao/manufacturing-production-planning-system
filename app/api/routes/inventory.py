from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import Inventory
from app.models.material_inventory import MaterialInventory
from app.schemas.inventory import MaterialInventoryResponse, ProductInventoryResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/product", response_model=list[ProductInventoryResponse])
def get_product_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return db.query(Inventory).offset(skip).limit(limit).all()


@router.get("/material", response_model=list[MaterialInventoryResponse])
def get_material_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return db.query(MaterialInventory).offset(skip).limit(limit).all()
