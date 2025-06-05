from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BranchBase(BaseModel):
    branch_name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    branch_id: int

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    hourly_rate: float
    hire_date: Optional[date] = None
    email: str

class EmployeeCreate(EmployeeBase):
    password: str

class Employee(EmployeeBase):
    employee_id: int
    branch_id: int
    is_active: bool

    class Config:
        from_attributes = True

class ShiftBase(BaseModel):
    shift_date: date
    start_time: time
    end_time: time
    is_approved: bool = False

class ShiftCreate(ShiftBase):
    employee_id: int

class Shift(ShiftBase):
    shift_id: int
    employee_id: int

    class Config:
        from_attributes = True

class PayrollBase(BaseModel):
    pay_period_start: date
    pay_period_end: date
    hours_worked: float
    overtime_hours: float = 0
    gross_pay: float

class PayrollCreate(PayrollBase):
    employee_id: int

class Payroll(PayrollBase):
    payroll_id: int
    employee_id: int

    class Config:
        from_attributes = True