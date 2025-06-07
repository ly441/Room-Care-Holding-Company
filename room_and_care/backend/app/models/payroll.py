from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from app.database import Base

class Payroll(Base):
    __tablename__ = "payroll"

    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    hours_worked = Column(Float, nullable=False)
    overtime_hours = Column(Float, default=0)
    gross_pay = Column(Float, nullable=False)