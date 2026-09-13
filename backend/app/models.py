from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class ValuationLog(Base):
    __tablename__ = "valuation_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    share_price = Column(Float, nullable=False)
    intrinsic_value = Column(Float, nullable=False)
    valuation_status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)