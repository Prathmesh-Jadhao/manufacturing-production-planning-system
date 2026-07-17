from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.production_plan import ProductionPlan
from app.schemas.production_plan import ProductionPlanResponse

router = APIRouter(prefix="/production-plans", tags=["Production Plans"])


@router.get("/", response_model=list[ProductionPlanResponse])
def get_production_plans(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db),
):
    return db.query(ProductionPlan).offset(skip).limit(limit).all()