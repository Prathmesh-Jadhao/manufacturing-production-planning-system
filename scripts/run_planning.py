from app.core.database import SessionLocal
from app.services.planning_engine import PlanningEngine


def main():
    db = SessionLocal()

    PlanningEngine.generate_plan(db)

    db.close()


if __name__ == "__main__":
    main()