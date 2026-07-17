from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(20), primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    family = Column(String(50), nullable=False)
    size_mm = Column(Integer, nullable=False)
    unit = Column(String(10), nullable=False, default="Nos")
    status = Column(String(20), nullable=False, default="Active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    bom_items = relationship(
        "BOM", back_populates="product", cascade="all, delete-orphan"
    )
    forecasts = relationship(
        "Forecast", back_populates="product", cascade="all, delete-orphan"
    )
    inventory = relationship(
        "Inventory", back_populates="product", cascade="all, delete-orphan"
    )
    production_plans = relationship(
        "ProductionPlan", back_populates="product", cascade="all, delete-orphan"
    )
    material_requirements = relationship(
        "MaterialRequirement", back_populates="product", cascade="all, delete-orphan"
    )