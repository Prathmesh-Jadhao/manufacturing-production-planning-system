import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Machine, MachineSchedule, ProductionPlan

logger = logging.getLogger(__name__)


class MachineScheduler:

    @staticmethod
    def generate_schedule(db: Session) -> dict:
        """Generate machine schedules from production plans.

        Fixes applied:
        - Tracks used capacity per machine across ALL plans
        - Guards against division by zero for zero-capacity machines
        - Uses settings.WORKING_DAYS instead of cross-service import
        - Returns summary data for API response
        """

        # Remove old schedules
        db.query(MachineSchedule).delete()
        db.commit()
        logger.info("Cleared previous machine schedules")

        # Only active machines, sorted by capacity (highest first)
        machines = (
            db.query(Machine)
            .filter(Machine.status == "Active")
            .order_by(Machine.daily_capacity.desc())
            .all()
        )

        if not machines:
            logger.warning("No active machines found")
            return {"schedules_created": 0}

        plans = (
            db.query(ProductionPlan)
            .filter(ProductionPlan.planned_quantity > 0)
            .all()
        )

        if not plans:
            logger.warning("No production plans with planned quantity > 0")
            return {"schedules_created": 0}

        # ----- Track capacity used per machine across all plans -----
        used_capacity = {m.machine_id: 0.0 for m in machines}

        schedules_created = 0

        for plan in plans:
            remaining_qty = float(plan.planned_quantity)

            for machine in machines:
                if remaining_qty <= 0:
                    break

                # Skip machines with zero capacity
                if machine.daily_capacity <= 0:
                    logger.warning(
                        "Machine %s has zero/negative capacity — skipping",
                        machine.machine_id,
                    )
                    continue

                machine_monthly_capacity = float(
                    machine.daily_capacity * settings.WORKING_DAYS
                )

                # Available = total capacity minus what's already been used
                available_capacity = max(
                    0.0, machine_monthly_capacity - used_capacity[machine.machine_id]
                )

                if available_capacity <= 0:
                    continue  # Machine fully allocated

                allocation = min(remaining_qty, available_capacity)

                utilization = (allocation / machine_monthly_capacity) * 100

                db.add(
                    MachineSchedule(
                        plan_id=plan.plan_id,
                        machine_id=machine.machine_id,
                        product_id=plan.product_id,
                        scheduled_quantity=allocation,
                        utilization=round(utilization, 2),
                        production_date=plan.plan_month,
                        status="SCHEDULED",
                    )
                )

                # Update tracking
                used_capacity[machine.machine_id] += allocation
                remaining_qty -= allocation
                schedules_created += 1

        db.commit()
        logger.info("Machine scheduling completed: %d schedules created", schedules_created)

        return {"schedules_created": schedules_created}