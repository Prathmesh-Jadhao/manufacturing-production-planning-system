from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base

class Forecast(Base):
    __tablename__ = "sales_forecasts"

    forecast_id = Column(Integer, primary_key=True, autoincrement=True)

    forecast_month = Column(Date, nullable=False)

    product_id = Column(
        ForeignKey("products.product_id"),
        nullable=False
    )

    forecast_qty = Column(Integer, nullable=False)

    product = relationship(
        "Product",
        back_populates="forecasts"
    )