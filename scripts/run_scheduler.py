import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.services.machine_scheduler import MachineScheduler


def main():
    db = SessionLocal()

    MachineScheduler.generate_schedule(db)

    db.close()


if __name__ == "__main__":
    main()