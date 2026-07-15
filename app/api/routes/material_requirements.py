from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.material_requirement import MaterialRequirement
from app.schemas.material_requirement import MaterialRequirementResponse

router = APIRouter(
    prefix="/material-requirements",
    tags=["Material Requirements"]
)


@router.get("/", response_model=list[MaterialRequirementResponse])
def get_material_requirements(db: Session = Depends(get_db)):
    return db.query(MaterialRequirement).all()