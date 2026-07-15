import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.services.planning_engine import PlanningEngine


def main():
    db = SessionLocal()

    PlanningEngine.generate_plan(db)

    db.close()


if __name__ == "__main__":
    main()