import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import Base, engine, SessionLocal
from app.core.logging import setup_logging
from app.models import *  # noqa: F401, F403
from scripts.seed_data import (
    load_products,
    load_materials,
    load_material_inventory,
    load_machines,
    load_bom,
    load_inventory,
    load_forecast,
)

setup_logging()
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        logger.info("Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        logger.info("Creating all tables from scratch...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Seeding database...")
        load_products(db)
        load_materials(db)
        load_material_inventory(db)
        load_machines(db)
        load_bom(db)
        load_inventory(db)
        load_forecast(db)
        
        logger.info("Database recreated and seeded successfully!")
    except Exception as e:
        logger.error("Failed to recreate/seed database: %s", e, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
