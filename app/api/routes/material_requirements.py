from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.material_requirement import MaterialRequirement
from app.schemas.material_requirement import MaterialRequirementResponse

router = APIRouter(prefix="/material-requirements", tags=["Material Requirements"])


@router.get("/", response_model=list[MaterialRequirementResponse])
def get_material_requirements(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db),
):
    return db.query(MaterialRequirement).offset(skip).limit(limit).all()