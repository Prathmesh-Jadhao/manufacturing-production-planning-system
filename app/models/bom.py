from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Date
)

from sqlalchemy.orm import relationship

from app.core.database import Base

class BOM(Base):
    __tablename__ = "bom"

    bom_id = Column(
        Integer,
        primary_key = True,
        autoincrement=True
    )

    product_id = Column(
        String(20),
        ForeignKey("products.product_id"),
        nullable=False
    )

    material_id = Column(
        String(20),
        ForeignKey("materials.material_id"),\
        nullable=False
    )

    quantity_per_unit = Column(
        Numeric(10,4),
        nullable=False
    )

    scrap_percentage = Column(
        Numeric(5,2),
        default=0
    )

    effective_from = Column(Date)

    effective_to = Column(Date)

    product = relationship(
        "Product",
        back_populates="bom_items"
    )

    material = relationship(
        "Material",
        back_populates="bom_items"
    )