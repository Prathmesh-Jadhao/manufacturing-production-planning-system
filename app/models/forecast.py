from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Forecast(Base):
    __tablename__ = "sales_forecasts"
    __table_args__ = (
        UniqueConstraint(
            "forecast_month", "product_id", name="uq_forecast_month_product"
        ),
        CheckConstraint("forecast_qty > 0", name="ck_forecast_qty_positive"),
    )

    forecast_id = Column(Integer, primary_key=True, autoincrement=True)
    forecast_month = Column(Date, nullable=False)
    product_id = Column(
        String(20), ForeignKey("products.product_id"), nullable=False
    )
    forecast_qty = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="forecasts")