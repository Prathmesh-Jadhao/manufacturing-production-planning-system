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


class ProductionPlan(Base):
    __tablename__ = "production_plans"

    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_month = Column(Date, nullable=False)
    product_id = Column(
        String(20), ForeignKey("products.product_id"), nullable=False
    )
    forecast_qty = Column(Integer, nullable=False)
    available_stock = Column(Integer, nullable=False)
    production_required = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    planned_quantity = Column(Integer, nullable=False)
    pending_quantity = Column(Integer, nullable=False)
    capacity_utilization = Column(Numeric(5, 2), nullable=False)
    status = Column(String(50), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    product = relationship("Product", back_populates="production_plans")
    material_requirements = relationship(
        "MaterialRequirement",
        back_populates="production_plan",
        cascade="all, delete-orphan",
    )
    machine_schedules = relationship(
        "MachineSchedule",
        back_populates="production_plan",
        cascade="all, delete-orphan",
    )