from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional

class ScanBase(BaseModel):
    filename: str

class ScanCreate(ScanBase):
    prediction: Any

class ScanUpdate(BaseModel):
    status: Optional[str] = None

class ScanResponse(ScanBase):
    id: int
    prediction: Any
    status: str
    created_at: datetime

    class Config:
        from_attributes = True