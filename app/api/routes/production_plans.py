from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.production_plan import ProductionPlan
from app.schemas.production_plan import ProductionPlanResponse

router = APIRouter(
    prefix="/production-plans",
    tags=["Production Plans"]
)


@router.get("/", response_model=list[ProductionPlanResponse])
def get_production_plans(db: Session = Depends(get_db)):
    return db.query(ProductionPlan).all()