from sqlalchemy.orm import Session

from app.models import (
    Machine,
    ProductionPlan,
    MachineSchedule
)
from app.services.planning_engine import PlanningEngine


class MachineScheduler:

    @staticmethod
    def generate_schedule(db: Session):

        # Remove old schedule
        db.query(MachineSchedule).delete()
        db.commit()

        # Only active machines
        machines = (
            db.query(Machine)
            .filter(Machine.status == "Active")
            .order_by(Machine.daily_capacity.desc())
            .all()
        )

        plans = (
            db.query(ProductionPlan)
            .filter(ProductionPlan.planned_quantity > 0)
            .all()
        )

        for plan in plans:

            remaining_qty = float(plan.planned_quantity)

            for machine in machines:

                if remaining_qty <= 0:
                    break

                machine_monthly_capacity = float(machine.daily_capacity * PlanningEngine.WORKING_DAYS)

                allocation = min(
                    remaining_qty,
                    machine_monthly_capacity
                )

                utilization = (
                    allocation /
                    machine_monthly_capacity
                ) * 100

                db.add(
                    MachineSchedule(
                        plan_id=plan.plan_id,
                        machine_id=machine.machine_id,
                        product_id=plan.product_id,
                        scheduled_quantity=allocation,
                        utilization=round(utilization, 2),
                        production_date=plan.plan_month,
                        status="SCHEDULED"
                    )
                )

                remaining_qty -= allocation

        db.commit()

        print("Machine Scheduling Completed")