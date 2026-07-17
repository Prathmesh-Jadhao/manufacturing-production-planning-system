import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.core.logging import setup_logging
from app.services.machine_scheduler import MachineScheduler

setup_logging()
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        result = MachineScheduler.generate_schedule(db)
        logger.info("Scheduler result: %s", result)
    except Exception as e:
        logger.error("Scheduling failed: %s", e, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()