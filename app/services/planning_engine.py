from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import (
    Forecast,
    Inventory,
    Machine,
    ProductionPlan,
    MaterialRequirement
)


class PlanningEngine:

    WORKING_DAYS = 22

    @staticmethod
    def generate_plan(db: Session):

        # Clear dependent table first
        db.query(MaterialRequirement).delete()
        db.commit()

        # Clear previous production plans
        db.query(ProductionPlan).delete()
        db.commit()

        # -----------------------------
        # Calculate Monthly Capacity
        # -----------------------------
        daily_capacity = (
            db.query(func.sum(Machine.daily_capacity))
            .scalar()
        ) or 0

        total_capacity = daily_capacity * PlanningEngine.WORKING_DAYS

        remaining_capacity = total_capacity

        forecasts = db.query(Forecast).all()

        planning_data = []

        # -----------------------------
        # Calculate Production Requirement
        # -----------------------------
        for forecast in forecasts:

            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.product_id == forecast.product_id
                )
                .first()
            )

            current_stock = (
                inventory.current_stock
                if inventory
                else 0
            )

            production_required = max(
                0,
                forecast.forecast_qty - current_stock
            )

            planning_data.append(
                {
                    "forecast": forecast,
                    "current_stock": current_stock,
                    "production_required": production_required,
                }
            )

        # Highest shortage gets priority
        planning_data.sort(
            key=lambda x: x["production_required"],
            reverse=True
        )

        # -----------------------------
        # Capacity Allocation
        # -----------------------------
        for item in planning_data:

            forecast = item["forecast"]
            current_stock = item["current_stock"]
            production_required = item["production_required"]

            planned_quantity = min(
                production_required,
                remaining_capacity
            )

            remaining_capacity -= planned_quantity

            pending_quantity = (
                production_required -
                planned_quantity
            )

            utilization = (
                (planned_quantity / total_capacity) * 100
                if total_capacity > 0
                else 0
            )

            status = (
                "READY"
                if pending_quantity == 0
                else "OVER_CAPACITY"
            )

            db.add(
                ProductionPlan(
                    plan_month=forecast.forecast_month,
                    product_id=forecast.product_id,
                    forecast_qty=forecast.forecast_qty,
                    available_stock=current_stock,
                    production_required=production_required,

                    # Monthly Plant Capacity
                    capacity=total_capacity,

                    planned_quantity=planned_quantity,
                    pending_quantity=pending_quantity,
                    capacity_utilization=round(utilization, 2),
                    status=status,
                )
            )

        db.commit()

        print("Production Planning Completed Successfully")