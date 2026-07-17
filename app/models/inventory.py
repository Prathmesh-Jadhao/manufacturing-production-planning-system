from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (
        CheckConstraint("opening_stock >= 0", name="ck_inv_opening_non_negative"),
        CheckConstraint("current_stock >= 0", name="ck_inv_current_non_negative"),
        CheckConstraint("safety_stock >= 0", name="ck_inv_safety_non_negative"),
    )

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        String(20), ForeignKey("products.product_id"), nullable=False, unique=True
    )
    opening_stock = Column(Integer, nullable=False)
    current_stock = Column(Integer, nullable=False)
    safety_stock = Column(Integer, nullable=False, default=0)
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    product = relationship("Product", back_populates="inventory")
