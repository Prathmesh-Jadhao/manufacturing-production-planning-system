from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MaterialInventory(Base):
    __tablename__ = "material_inventory"
    __table_args__ = (
        CheckConstraint(
            "available_stock >= 0", name="ck_matinv_stock_non_negative"
        ),
        CheckConstraint(
            "reorder_level >= 0", name="ck_matinv_reorder_non_negative"
        ),
    )

    material_id = Column(
        String(20), ForeignKey("materials.material_id"), primary_key=True
    )
    available_stock = Column(Numeric(12, 4), nullable=False)
    reorder_level = Column(Numeric(12, 4), nullable=False)
    location = Column(String(50), nullable=False)
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    material = relationship("Material", back_populates="inventory", uselist=False)