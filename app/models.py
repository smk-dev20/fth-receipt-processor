from database import Base
from sqlalchemy import Column, JSON, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

class Receipt(Base):
    __tablename__  = "receipts"
    id = Column(String(255), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    input_receipt = Column(JSON, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, default=func.now())  

    points = relationship("Point", back_populates="receipt")

class Point(Base):
    __tablename__ = "points"
    id = Column(String(255), primary_key=True, unique=True, index= True, default=lambda: str(uuid.uuid4()))
    receipt_id = Column(String(255), ForeignKey("receipts.id"), nullable=False)
    awarded_points = Column(Integer, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, default=func.now())  
    
    receipt = relationship("Receipt", back_populates="points")