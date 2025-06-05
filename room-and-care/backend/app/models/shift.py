from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Shift(Base):
    __tablename__ = "shifts"

    shift_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    shift_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_approved = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="shifts")