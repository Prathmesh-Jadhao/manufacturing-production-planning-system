import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.core.logging import setup_logging
from app.services.planning_engine import PlanningEngine

setup_logging()
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        result = PlanningEngine.generate_plan(db)
        logger.info("Planning result: %s", result)
    except Exception as e:
        logger.error("Planning failed: %s", e, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()