import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import MachineSchedule
from app.schemas.machine_schedule import MachineScheduleResponse
from app.services.machine_scheduler import MachineScheduler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/schedule", tags=["Machine Scheduling"])


@router.post("/run")
def run_scheduler(db: Session = Depends(get_db)):
    try:
        result = MachineScheduler.generate_schedule(db)
        return {
            "message": "Machine schedule generated successfully.",
            **result,
        }
    except Exception as e:
        logger.error("Machine scheduler failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Machine scheduling failed. Check server logs for details.",
        )


@router.get("/", response_model=list[MachineScheduleResponse])
def get_schedule(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return db.query(MachineSchedule).offset(skip).limit(limit).all()