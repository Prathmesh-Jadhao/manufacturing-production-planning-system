from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(
        ForeignKey("products.product_id"),
        nullable=False
    )

    opening_stock = Column(Integer, nullable=False)

    current_stock = Column(Integer, nullable=False)

    safety_stock = Column(Integer, default=0)

    last_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    product = relationship(
        "Product",
        back_populates="inventory"
    )

