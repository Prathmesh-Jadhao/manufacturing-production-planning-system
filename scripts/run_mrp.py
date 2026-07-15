import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.services.mrp_engine import MRPEngine


def main():

    db = SessionLocal()

    MRPEngine.generate_mrp(db)

    db.close()


if __name__ == "__main__":
    main()