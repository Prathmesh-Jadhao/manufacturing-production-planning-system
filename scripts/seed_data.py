import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from app.core.database import SessionLocal
from app.models import (
    Product,
    Material,
    MaterialInventory,
    Machine,
    BOM,
    Inventory,
    Forecast
)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw"


def load_products(db):
    df = pd.read_csv(RAW_DATA / "products.csv")

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

    db.commit()
    print("Products Loaded")


def load_materials(db):
    df = pd.read_csv(RAW_DATA / "materials.csv")

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

    db.commit()
    print("Materials Loaded")


def load_material_inventory(db):

    df = pd.read_csv(RAW_DATA / "material_inventory.csv")

    for _, row in df.iterrows():

        exists = (
            db.query(MaterialInventory)
            .filter(
                MaterialInventory.material_id == row["material_id"]
            )
            .first()
        )

        if exists:
            continue

        db.add(
            MaterialInventory(
                material_id=row["material_id"],
                available_stock=row["available_stock"],
                reorder_level=row["reorder_level"],
                location=row["location"]
            )
        )

    db.commit()

    print("Material Inventory Loaded")


def load_machines(db):
    df = pd.read_csv(RAW_DATA / "machines.csv")

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

    db.commit()
    print("Machines Loaded")


def load_bom(db):
    df = pd.read_csv(RAW_DATA / "bom.csv")

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

    db.commit()
    print("BOM Loaded")


def load_inventory(db):
    df = pd.read_csv(RAW_DATA / "inventory.csv")

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

    db.commit()
    print("Inventory Loaded")


def load_forecast(db):
    df = pd.read_csv(RAW_DATA / "forecast.csv")
    df["forecast_month"] = pd.to_datetime(df["forecast_month"])

    for _, row in df.iterrows():

        db.add(
            Forecast(
                forecast_month=row["forecast_month"],
                product_id=row["product_id"],
                forecast_qty=row["forecast_qty"],
            )
        )

    db.commit()
    print("Forecast Loaded")


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

        print("\nDatabase Seeded Successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    main()