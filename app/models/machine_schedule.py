from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MachineSchedule(Base):
    __tablename__ = "machine_schedule"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(
        Integer, ForeignKey("production_plans.plan_id"), nullable=False
    )
    machine_id = Column(
        String(20), ForeignKey("machines.machine_id"), nullable=False
    )
    product_id = Column(
        String(20), ForeignKey("products.product_id"), nullable=False
    )
    scheduled_quantity = Column(Numeric(10, 2), nullable=False)
    utilization = Column(Numeric(5, 2), nullable=False)
    production_date = Column(Date, nullable=False)
    status = Column(String(30), nullable=False, default="SCHEDULED")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    machine = relationship("Machine", back_populates="schedules")
    production_plan = relationship("ProductionPlan", back_populates="machine_schedules")
    product = relationship("Product")