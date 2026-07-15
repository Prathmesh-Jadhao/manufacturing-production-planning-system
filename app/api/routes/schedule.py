from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.machine_scheduler import MachineScheduler
from app.models import MachineSchedule

router = APIRouter(
    prefix="/schedule",
    tags=["Machine Scheduling"]
)


@router.post("/run")
def run_scheduler(db: Session = Depends(get_db)):
    MachineScheduler.generate_schedule(db)

    return {
        "message": "Machine schedule generated successfully."
    }


@router.get("/")
def get_schedule(db: Session = Depends(get_db)):
    return db.query(MachineSchedule).all()