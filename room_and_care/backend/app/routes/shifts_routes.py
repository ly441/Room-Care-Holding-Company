
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List  # ✅ Correct import for Python 3.8

from app.database import get_db
from app.models.shift import Shift as ShiftModel  # ✅ Avoid name clash
from app.schemas.schemas import ShiftCreate, Shift  # Pydantic schema
from app.models.employee import Employee

router = APIRouter()

@router.post("/", response_model=Shift)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == shift.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    overlapping = db.query(ShiftModel).filter(
        ShiftModel.employee_id == shift.employee_id,
        ShiftModel.shift_date == shift.shift_date,
        (
            (ShiftModel.start_time <= shift.start_time) & (ShiftModel.end_time > shift.start_time) |
            (ShiftModel.start_time < shift.end_time) & (ShiftModel.end_time >= shift.end_time) |
            (ShiftModel.start_time >= shift.start_time) & (ShiftModel.end_time <= shift.end_time)
        )
    ).first()
    
    if overlapping:
        raise HTTPException(status_code=400, detail="Shift overlaps with existing shift for this employee")
    
    db_shift = ShiftModel(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@router.get("/", response_model=List[Shift])  # ✅ Corrected
def read_shifts(
    start_date: date = None,
    end_date: date = None,
    employee_id: int = None,
    branch_id: int = None,
    approved_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(ShiftModel)
    
    if approved_only:
        query = query.filter(ShiftModel.is_approved == True)
    
    if start_date:
        query = query.filter(ShiftModel.shift_date >= start_date)
    
    if end_date:
        query = query.filter(ShiftModel.shift_date <= end_date)
    
    if employee_id:
        query = query.filter(ShiftModel.employee_id == employee_id)
    
    if branch_id:
        query = query.join(Employee).filter(Employee.branch_id == branch_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{shift_id}", response_model=Shift)
def read_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(ShiftModel).filter(ShiftModel.shift_id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift

@router.put("/{shift_id}", response_model=Shift)
def update_shift(shift_id: int, shift_update: ShiftCreate, db: Session = Depends(get_db)):
    db_shift = db.query(ShiftModel).filter(ShiftModel.shift_id == shift_id).first()
    if not db_shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    employee = db.query(Employee).filter(Employee.employee_id == shift_update.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    overlapping = db.query(ShiftModel).filter(
        ShiftModel.shift_id != shift_id,
        ShiftModel.employee_id == shift_update.employee_id,
        ShiftModel.shift_date == shift_update.shift_date,
        (
            (ShiftModel.start_time <= shift_update.start_time) & (ShiftModel.end_time > shift_update.start_time) |
            (ShiftModel.start_time < shift_update.end_time) & (ShiftModel.end_time >= shift_update.end_time) |
            (ShiftModel.start_time >= shift_update.start_time) & (ShiftModel.end_time <= shift_update.end_time)
        )
    ).first()
    
    if overlapping:
        raise HTTPException(status_code=400, detail="Shift overlaps with existing shift for this employee")
    
    for key, value in shift_update.dict().items():
        setattr(db_shift, key, value)
    
    db.commit()
    db.refresh(db_shift)
    return db_shift

@router.patch("/{shift_id}/approve", response_model=Shift)
def approve_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(ShiftModel).filter(ShiftModel.shift_id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    shift.is_approved = True
    db.commit()
    db.refresh(shift)
    return shift

@router.delete("/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(ShiftModel).filter(ShiftModel.shift_id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    db.delete(shift)
    db.commit()
    return {"message": "Shift deleted"}
