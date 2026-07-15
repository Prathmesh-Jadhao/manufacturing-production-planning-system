from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Machine(Base):
    __tablename__ = "machines"

    machine_id = Column(
        String(20),
        primary_key=True,
        index=True
    )

    machine_name = Column(
        String(100),
        nullable=False
    )

    line_name = Column(
        String(50),
        nullable=False
    )

    daily_capacity = Column(
        Integer,
        nullable=False
    )

    shift_hours = Column(
        Integer,
        nullable=False,
        default=8
    )

    status = Column(
        String(20),
        nullable=False,
        default="Active"
    )