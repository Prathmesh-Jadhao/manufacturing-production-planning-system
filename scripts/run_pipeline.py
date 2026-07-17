"""
Manufacturing Pipeline Runner
==============================
Executes the full production planning pipeline in sequence:

  Step 1: Production Planning  (Forecast -> Capacity-constrained plans)
  Step 2: MRP                  (Plans -> Raw material requirements)
  Step 3: Machine Scheduling   (Plans -> Machine-level allocations)

Usage:
    python scripts/run_pipeline.py
"""

import logging
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.core.logging import setup_logging
from app.services.planning_engine import PlanningEngine
from app.services.mrp_engine import MRPEngine
from app.services.machine_scheduler import MachineScheduler

setup_logging()
logger = logging.getLogger(__name__)

SEPARATOR = "=" * 60
DASH = "-" * 50


def run_pipeline():
    """Run the full manufacturing pipeline: Planning -> MRP -> Scheduling."""

    print(f"\n{SEPARATOR}")
    print("  MANUFACTURING PRODUCTION PLANNING PIPELINE")
    print(SEPARATOR)

    db = SessionLocal()
    start_time = time.time()

    try:
        # -- Step 1: Production Planning --------------------------
        print(f"\n{DASH}")
        print("  [Step 1/3] Running Production Planning Engine...")
        print(DASH)

        step_start = time.time()
        planning_result = PlanningEngine.generate_plan(db)
        step_time = time.time() - step_start

        print(f"  [OK] Plans Created     : {planning_result['plans_created']}")
        print(f"       Total Capacity    : {planning_result['total_capacity']:,} units")
        print(f"       Remaining Cap.    : {planning_result['remaining_capacity']:,} units")
        print(f"       Completed in      : {step_time:.2f}s")

        if planning_result["plans_created"] == 0:
            print("\n  [WARN] No plans created -- pipeline cannot continue.")
            print("  [TIP]  Make sure forecasts are loaded (run seed_data.py first).")
            return

        # -- Step 2: MRP (Material Requirements Planning) ---------
        print(f"\n{DASH}")
        print("  [Step 2/3] Running MRP Engine...")
        print(DASH)

        step_start = time.time()
        mrp_result = MRPEngine.generate_mrp(db)
        step_time = time.time() - step_start

        print(f"  [OK] Requirements      : {mrp_result['requirements_created']}")
        print(f"       Shortages         : {mrp_result['shortages']}")
        print(f"       Completed in      : {step_time:.2f}s")

        # -- Step 3: Machine Scheduling ---------------------------
        print(f"\n{DASH}")
        print("  [Step 3/3] Running Machine Scheduler...")
        print(DASH)

        step_start = time.time()
        schedule_result = MachineScheduler.generate_schedule(db)
        step_time = time.time() - step_start

        print(f"  [OK] Schedules Created : {schedule_result['schedules_created']}")
        print(f"       Completed in      : {step_time:.2f}s")

        # -- Summary ----------------------------------------------
        total_time = time.time() - start_time

        print(f"\n{SEPARATOR}")
        print("  PIPELINE COMPLETED SUCCESSFULLY")
        print(SEPARATOR)
        print(f"  Production Plans     : {planning_result['plans_created']}")
        print(f"  Material Reqs        : {mrp_result['requirements_created']}")
        print(f"  Shortages            : {mrp_result['shortages']}")
        print(f"  Machine Schedules    : {schedule_result['schedules_created']}")
        print(f"  Total Time           : {total_time:.2f}s")
        print(SEPARATOR)
        print()

    except Exception as e:
        logger.error("Pipeline failed: %s", e, exc_info=True)
        db.rollback()
        print(f"\n  [FAILED] PIPELINE FAILED: {e}")
        print("  Check logs for details.\n")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_pipeline()
