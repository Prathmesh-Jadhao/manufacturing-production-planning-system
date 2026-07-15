from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.planning_engine import PlanningEngine

router = APIRouter(
    prefix="/planning",
    tags=["Planning"]
)

@router.post("/run")
def run_planning(db: Session = Depends(get_db)):
    try:
        PlanningEngine.generate_plan(db)
        return {"message": "Production planning generated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))