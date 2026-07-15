from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Date,
)

from sqlalchemy.orm import relationship

from app.core.database import Base

from sqlalchemy import DateTime
from sqlalchemy.sql import func

class MaterialRequirement(Base):
    __tablename__ = "material_requirements"

    requirement_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    plan_id = Column(
        Integer,
        ForeignKey("production_plans.plan_id"),
        nullable=False,
        index=True
    )

    product_id = Column(
        String(20),
        ForeignKey("products.product_id"),
        nullable=False,
        index=True
    )

    material_id = Column(
        String(20),
        ForeignKey("materials.material_id"),
        nullable=False,
        index=True
    )

    required_quantity = Column(
        Numeric(12,4),
        nullable=False
    )

    available_stock = Column(
        Numeric(12,4),
        nullable=False
    )

    shortage_quantity = Column(
        Numeric(12,4),
        nullable=False
    )

    procurement_required = Column(
        Numeric(12,4),
        nullable=False
    )

    procurement_status = Column(
        String(30),
        nullable=False
    )

    unit = Column(
        String(20),
        nullable=False
    )

    requirement_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(30),
        default="PENDING",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    product = relationship(
        "Product",
        back_populates="material_requirements"
    )

    material = relationship(
        "Material",
        back_populates="material_requirements"
    )

    production_plan = relationship(
        "ProductionPlan",
        back_populates="material_requirements"
    )