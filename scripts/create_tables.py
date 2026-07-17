import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import Base, engine
from app.core.logging import setup_logging
from app.models import *  # noqa: F401, F403 — registers all models with Base

setup_logging()
logger = logging.getLogger(__name__)


def main():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error("Failed to create tables: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    main()