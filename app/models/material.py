from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base

class Material(Base):
    __tablename__ = "materials"

    material_id = Column(String(20), primary_key=True, index=True)

    material_name = Column(String(100), nullable=False)

    unit = Column(String(20), nullable=False)

    bom_items = relationship(
        "BOM",
        back_populates="material",
        cascade="all, delete-orphan"
    )

    material_requirements = relationship(
        "MaterialRequirement",
        back_populates="material",
        cascade="all, delete-orphan"
    )

    inventory = relationship(
        "MaterialInventory",
        back_populates="material",
        uselist=False,
        cascade="all, delete-orphan"
    )