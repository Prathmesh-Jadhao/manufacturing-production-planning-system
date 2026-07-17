from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Material(Base):
    __tablename__ = "materials"

    material_id = Column(String(20), primary_key=True, index=True)
    material_name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="Active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    bom_items = relationship(
        "BOM", back_populates="material", cascade="all, delete-orphan"
    )
    material_requirements = relationship(
        "MaterialRequirement", back_populates="material", cascade="all, delete-orphan"
    )
    inventory = relationship(
        "MaterialInventory",
        back_populates="material",
        uselist=False,
        cascade="all, delete-orphan",
    )