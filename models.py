from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    prediction = Column(JSON)  # Stores the full Roboflow response
    status = Column(String, default="processed")
    created_at = Column(DateTime, default=datetime.utcnow)