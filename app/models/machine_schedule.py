from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class MachineSchedule(Base):
    __tablename__ = "machine_schedule"

    schedule_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    plan_id = Column(
        Integer,
        ForeignKey("production_plans.plan_id"),
        nullable=False
    )

    machine_id = Column(
        String(20),
        ForeignKey("machines.machine_id"),
        nullable=False
    )

    product_id = Column(
        String(20),
        ForeignKey("products.product_id"),
        nullable=False
    )

    scheduled_quantity = Column(
        Numeric(10,2),
        nullable=False
    )

    utilization = Column(
        Numeric(5,2),
        nullable=False
    )

    production_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(30),
        default="SCHEDULED"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    machine = relationship("Machine")
    production_plan = relationship("ProductionPlan")
    product = relationship("Product")