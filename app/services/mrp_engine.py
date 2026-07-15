from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import (
    BOM,
    MaterialInventory,
    MaterialRequirement,
    ProductionPlan,
)


class MRPEngine:

    @staticmethod
    def generate_mrp(db: Session):

        # Clear previous MRP
        db.query(MaterialRequirement).delete()
        db.commit()

        production_plans = (
            db.query(ProductionPlan)
            .filter(ProductionPlan.planned_quantity > 0)
            .all()
        )

        for plan in production_plans:

            bom_items = (
                db.query(BOM)
                .filter(BOM.product_id == plan.product_id)
                .all()
            )

            for bom in bom_items:

                required_qty = (
                    Decimal(plan.planned_quantity)
                    * Decimal(bom.quantity_per_unit)
                )

                inventory = (
                    db.query(MaterialInventory)
                    .filter(
                        MaterialInventory.material_id == bom.material_id
                    )
                    .first()
                )

                available_stock = (
                    Decimal(inventory.available_stock)
                    if inventory
                    else Decimal("0")
                )

                reorder_level = (
                    Decimal(inventory.reorder_level)
                    if inventory
                    else Decimal("0")
                )

                usable_stock = max(
                    Decimal("0"),
                    available_stock - reorder_level
                )

                shortage = max(
                    Decimal("0"),
                    required_qty - usable_stock
                )

                procurement_required = shortage

                procurement_status = (
                    "OK"
                    if shortage == 0
                    else "PROCUREMENT_REQUIRED"
                )

                material_requirement = MaterialRequirement(

                    plan_id=plan.plan_id,

                    product_id=plan.product_id,

                    material_id=bom.material_id,

                    required_quantity=required_qty,

                    available_stock=available_stock,

                    shortage_quantity=shortage,

                    procurement_required=procurement_required,

                    procurement_status=procurement_status,

                    unit=bom.material.unit,

                    requirement_date=plan.plan_month,

                    status="GENERATED"
                )

                db.add(material_requirement)

        db.commit()

        print("\nMRP Generated Successfully")