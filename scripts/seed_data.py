import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from app.core.database import SessionLocal
from app.core.logging import setup_logging
from app.models import (
    BOM,
    Forecast,
    Inventory,
    Machine,
    Material,
    MaterialInventory,
    Product,
)

setup_logging()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw"


def _read_csv(filename: str) -> pd.DataFrame:
    """Read a CSV file with error handling."""
    filepath = RAW_DATA / filename
    if not filepath.exists():
        logger.error("CSV file not found: %s", filepath)
        raise FileNotFoundError(f"Required data file missing: {filepath}")
    df = pd.read_csv(filepath)
    # Drop fully empty rows (handles blank lines in CSVs like bom.csv)
    df = df.dropna(how="all")
    return df


def load_products(db):
    df = _read_csv("products.csv")
    count = 0
    for _, row in df.iterrows():
        exists = db.query(Product).filter(
            Product.product_id == row["product_id"]
        ).first()
        if exists:
            continue
        db.add(
            Product(
                product_id=row["product_id"],
                product_name=row["product_name"],
                family=row["family"],
                size_mm=row["size_mm"],
                unit=row["unit"],
                status=row["status"],
            )
        )
        count += 1
    db.commit()
    logger.info("Products loaded: %d new records", count)


def load_materials(db):
    df = _read_csv("materials.csv")
    count = 0
    for _, row in df.iterrows():
        exists = db.query(Material).filter(
            Material.material_id == row["material_id"]
        ).first()
        if exists:
            continue
        db.add(
            Material(
                material_id=row["material_id"],
                material_name=row["material_name"],
                unit=row["unit"],
            )
        )
        count += 1
    db.commit()
    logger.info("Materials loaded: %d new records", count)


def load_material_inventory(db):
    df = _read_csv("material_inventory.csv")
    count = 0
    for _, row in df.iterrows():
        exists = (
            db.query(MaterialInventory)
            .filter(MaterialInventory.material_id == row["material_id"])
            .first()
        )
        if exists:
            continue
        db.add(
            MaterialInventory(
                material_id=row["material_id"],
                available_stock=row["available_stock"],
                reorder_level=row["reorder_level"],
                location=row["location"],
            )
        )
        count += 1
    db.commit()
    logger.info("Material inventory loaded: %d new records", count)


def load_machines(db):
    df = _read_csv("machines.csv")
    count = 0
    for _, row in df.iterrows():
        exists = db.query(Machine).filter(
            Machine.machine_id == row["machine_id"]
        ).first()
        if exists:
            continue
        db.add(
            Machine(
                machine_id=row["machine_id"],
                machine_name=row["machine_name"],
                line_name=row["line_name"],
                daily_capacity=row["daily_capacity"],
                shift_hours=row["shift_hours"],
                status=row["status"],
            )
        )
        count += 1
    db.commit()
    logger.info("Machines loaded: %d new records", count)


def load_bom(db):
    df = _read_csv("bom.csv")
    count = 0
    for _, row in df.iterrows():
        exists = (
            db.query(BOM)
            .filter(
                BOM.product_id == row["product_id"],
                BOM.material_id == row["material_id"],
            )
            .first()
        )
        if exists:
            continue
        db.add(
            BOM(
                product_id=row["product_id"],
                material_id=row["material_id"],
                quantity_per_unit=row["quantity_per_unit"],
                scrap_percentage=row["scrap_percentage"],
            )
        )
        count += 1
    db.commit()
    logger.info("BOM loaded: %d new records", count)


def load_inventory(db):
    df = _read_csv("inventory.csv")
    count = 0
    for _, row in df.iterrows():
        exists = (
            db.query(Inventory)
            .filter(Inventory.product_id == row["product_id"])
            .first()
        )
        if exists:
            continue
        db.add(
            Inventory(
                product_id=row["product_id"],
                opening_stock=row["opening_stock"],
                current_stock=row["current_stock"],
                safety_stock=row["safety_stock"],
            )
        )
        count += 1
    db.commit()
    logger.info("Inventory loaded: %d new records", count)


def load_forecast(db):
    df = _read_csv("forecast.csv")
    df["forecast_month"] = pd.to_datetime(df["forecast_month"])
    count = 0
    for _, row in df.iterrows():
        # Duplicate check — same pattern as other loaders
        exists = (
            db.query(Forecast)
            .filter(
                Forecast.forecast_month == row["forecast_month"],
                Forecast.product_id == row["product_id"],
            )
            .first()
        )
        if exists:
            continue
        db.add(
            Forecast(
                forecast_month=row["forecast_month"],
                product_id=row["product_id"],
                forecast_qty=row["forecast_qty"],
            )
        )
        count += 1
    db.commit()
    logger.info("Forecasts loaded: %d new records", count)


def main():
    db = SessionLocal()
    try:
        load_products(db)
        load_materials(db)
        load_material_inventory(db)
        load_machines(db)
        load_bom(db)
        load_inventory(db)
        load_forecast(db)
        logger.info("Database seeded successfully!")
    except Exception as e:
        logger.error("Seeding failed: %s", e, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()