from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.mrp_engine import MRPEngine

router = APIRouter(
    prefix="/mrp",
    tags=["MRP"]
)


@router.post("/run")
def run_mrp(db: Session = Depends(get_db)):
    MRPEngine.generate_mrp(db)

    return {
        "message": "MRP generated successfully."
    }