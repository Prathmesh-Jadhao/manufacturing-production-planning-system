import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.core.logging import setup_logging
from app.services.mrp_engine import MRPEngine

setup_logging()
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        result = MRPEngine.generate_mrp(db)
        logger.info("MRP result: %s", result)
    except Exception as e:
        logger.error("MRP failed: %s", e, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()