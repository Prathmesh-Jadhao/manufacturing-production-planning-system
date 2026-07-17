import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.mrp_engine import MRPEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mrp", tags=["MRP"])


@router.post("/run")
def run_mrp(db: Session = Depends(get_db)):
    try:
        result = MRPEngine.generate_mrp(db)
        return {
            "message": "MRP generated successfully.",
            **result,
        }
    except Exception as e:
        logger.error("MRP engine failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="MRP generation failed. Check server logs for details.",
        )