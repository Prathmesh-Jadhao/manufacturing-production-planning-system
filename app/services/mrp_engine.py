import logging
from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models import (
    BOM,
    MaterialInventory,
    MaterialRequirement,
    ProductionPlan,
)

logger = logging.getLogger(__name__)


class MRPEngine:

    @staticmethod
    def generate_mrp(db: Session) -> dict:
        """Generate material requirements from production plans.

        Fixes applied:
        - Accounts for scrap percentage in quantity calculation
        - Tracks material allocation across all plans to prevent double-counting
        - Eager-loads BOM.material to avoid N+1 queries
        - Returns summary data for API response
        """

        # Clear previous MRP data
        db.query(MaterialRequirement).delete()
        db.commit()
        logger.info("Cleared previous material requirements")

        production_plans = (
            db.query(ProductionPlan)
            .filter(ProductionPlan.planned_quantity > 0)
            .all()
        )

        if not production_plans:
            logger.warning("No production plans with planned quantity > 0")
            return {"requirements_created": 0, "shortages": 0}

        # ----- Track allocated material across ALL plans -----
        # material_id -> total quantity already allocated
        allocated = {}

        requirements_created = 0
        shortages = 0

        for plan in production_plans:
            # Eager-load material relationship via joinedload
            bom_items = (
                db.query(BOM)
                .options(joinedload(BOM.material))
                .filter(BOM.product_id == plan.product_id)
                .all()
            )

            for bom in bom_items:
                # Account for scrap percentage
                scrap_factor = Decimal(1) + (
                    Decimal(bom.scrap_percentage or 0) / Decimal(100)
                )
                required_qty = (
                    Decimal(plan.planned_quantity)
                    * Decimal(bom.quantity_per_unit)
                    * scrap_factor
                )

                # Get material inventory
                inventory = (
                    db.query(MaterialInventory)
                    .filter(MaterialInventory.material_id == bom.material_id)
                    .first()
                )

                available_stock = (
                    Decimal(inventory.available_stock) if inventory else Decimal(0)
                )
                reorder_level = (
                    Decimal(inventory.reorder_level) if inventory else Decimal(0)
                )

                # Track how much of this material has already been allocated
                already_allocated = allocated.get(bom.material_id, Decimal(0))

                # Usable stock = available - reorder level - already allocated
                usable_stock = max(
                    Decimal(0),
                    available_stock - reorder_level - already_allocated,
                )

                shortage = max(Decimal(0), required_qty - usable_stock)
                procurement_required = shortage

                procurement_status = (
                    "OK" if shortage == 0 else "PROCUREMENT_REQUIRED"
                )

                # Update allocation tracker
                allocated[bom.material_id] = already_allocated + min(
                    required_qty, usable_stock + shortage
                )

                db.add(
                    MaterialRequirement(
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
                        status="GENERATED",
                    )
                )
                requirements_created += 1
                if shortage > 0:
                    shortages += 1

        db.commit()
        logger.info(
            "MRP completed: %d requirements created, %d shortages found",
            requirements_created,
            shortages,
        )

        return {
            "requirements_created": requirements_created,
            "shortages": shortages,
        }