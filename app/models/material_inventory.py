from sqlalchemy import Column, String, Numeric

from sqlalchemy.orm import relationship

from app.core.database import Base

from sqlalchemy import ForeignKey

class MaterialInventory(Base):
    __tablename__ = "material_inventory"

    material_id = Column(
        String(20),
        ForeignKey("materials.material_id"),
        primary_key=True
    )

    available_stock = Column(
        Numeric(12,4),
        nullable=False
    )

    reorder_level = Column(
        Numeric(12,4),
        nullable=False
    )

    location = Column(
        String(50),
        nullable=False
    )

    material = relationship(
        "Material",
        back_populates="inventory",
        uselist=False
    )