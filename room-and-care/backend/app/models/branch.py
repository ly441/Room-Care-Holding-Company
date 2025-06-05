from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String(50), nullable=False)
    address = Column(Text)
    phone = Column(String(15))