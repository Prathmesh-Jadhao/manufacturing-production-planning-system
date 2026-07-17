import logging
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import (
    Forecast,
    Inventory,
    Machine,
    MachineSchedule,
    MaterialRequirement,
    ProductionPlan,
)

logger = logging.getLogger(__name__)


class PlanningEngine:

    @staticmethod
    def generate_plan(db: Session) -> dict:
        """Generate production plans from forecasts against machine capacity.

        Fixes applied:
        - Accounts for safety stock when calculating production required
        - Only counts ACTIVE machines for capacity
        - Uses single transaction for cleanup deletes
        - Returns summary data for API response
        """

        # ----- Clear previous data in single transaction -----
        db.query(MachineSchedule).delete()
        db.query(MaterialRequirement).delete()
        db.query(ProductionPlan).delete()
        db.commit()
        logger.info("Cleared previous plans, requirements, and schedules")

        # ----- Calculate Monthly Capacity (ACTIVE machines only) -----
        daily_capacity = (
            db.query(func.sum(Machine.daily_capacity))
            .filter(Machine.status == "Active")
            .scalar()
        ) or 0

        total_capacity = daily_capacity * settings.WORKING_DAYS
        remaining_capacity = total_capacity
        logger.info(
            "Total monthly capacity: %d (from active machines, %d working days)",
            total_capacity,
            settings.WORKING_DAYS,
        )

        # ----- Fetch forecasts -----
        forecasts = db.query(Forecast).all()

        if not forecasts:
            logger.warning("No forecasts found — nothing to plan")
            return {"plans_created": 0, "total_capacity": total_capacity}

        # ----- Calculate Production Requirements -----
        planning_data = []

        for forecast in forecasts:
            inventory = (
                db.query(Inventory)
                .filter(Inventory.product_id == forecast.product_id)
                .first()
            )

            current_stock = inventory.current_stock if inventory else 0
            safety_stock = inventory.safety_stock if inventory else 0

            # Net available = current stock minus safety buffer
            net_available = max(0, current_stock - safety_stock)

            production_required = max(0, forecast.forecast_qty - net_available)

            planning_data.append(
                {
                    "forecast": forecast,
                    "current_stock": current_stock,
                    "safety_stock": safety_stock,
                    "production_required": production_required,
                }
            )

        # Highest shortage gets priority
        planning_data.sort(key=lambda x: x["production_required"], reverse=True)

        # ----- Capacity Allocation -----
        plans_created = 0

        for item in planning_data:
            forecast = item["forecast"]
            current_stock = item["current_stock"]
            production_required = item["production_required"]

            planned_quantity = min(production_required, remaining_capacity)
            remaining_capacity -= planned_quantity

            pending_quantity = production_required - planned_quantity

            utilization = (
                (planned_quantity / total_capacity) * 100
                if total_capacity > 0
                else 0
            )

            status = "READY" if pending_quantity == 0 else "OVER_CAPACITY"

            db.add(
                ProductionPlan(
                    plan_month=forecast.forecast_month,
                    product_id=forecast.product_id,
                    forecast_qty=forecast.forecast_qty,
                    available_stock=current_stock,
                    production_required=production_required,
                    capacity=total_capacity,
                    planned_quantity=planned_quantity,
                    pending_quantity=pending_quantity,
                    capacity_utilization=round(utilization, 2),
                    status=status,
                )
            )
            plans_created += 1

        db.commit()
        logger.info(
            "Production planning completed: %d plans created, remaining capacity: %d",
            plans_created,
            remaining_capacity,
        )

        return {
            "plans_created": plans_created,
            "total_capacity": total_capacity,
            "remaining_capacity": remaining_capacity,
        }