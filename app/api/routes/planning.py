import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.planning_engine import PlanningEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/planning", tags=["Planning"])


@router.post("/run")
def run_planning(db: Session = Depends(get_db)):
    try:
        result = PlanningEngine.generate_plan(db)
        return {
            "message": "Production planning generated successfully.",
            **result,
        }
    except Exception as e:
        logger.error("Planning engine failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Production planning failed. Check server logs for details.",
        )