from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.material import Material
from app.schemas.material import MaterialResponse

router = APIRouter(prefix="/materials", tags=["Materials"])


@router.get("/", response_model=list[MaterialResponse])
def get_materials(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db),
):
    return db.query(Material).offset(skip).limit(limit).all()