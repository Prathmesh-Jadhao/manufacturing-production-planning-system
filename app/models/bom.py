from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class BOM(Base):
    __tablename__ = "bom"
    __table_args__ = (
        UniqueConstraint("product_id", "material_id", name="uq_bom_product_material"),
        CheckConstraint("quantity_per_unit > 0", name="ck_bom_qty_positive"),
        CheckConstraint("scrap_percentage >= 0", name="ck_bom_scrap_non_negative"),
    )

    bom_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        String(20), ForeignKey("products.product_id"), nullable=False, index=True
    )
    material_id = Column(
        String(20), ForeignKey("materials.material_id"), nullable=False, index=True
    )
    quantity_per_unit = Column(Numeric(10, 4), nullable=False)
    scrap_percentage = Column(Numeric(5, 2), default=0)
    effective_from = Column(Date)
    effective_to = Column(Date)

    product = relationship("Product", back_populates="bom_items")
    material = relationship("Material", back_populates="bom_items")