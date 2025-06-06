
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.shift import Shift
from app.schemas.schemas import ShiftCreate, Shift
from app.models.employee import Employee

router = APIRouter()

@router.post("/", response_model=Shift)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    # Check if employee exists
    employee = db.query(Employee).filter(Employee.employee_id == shift.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check for overlapping shifts
    overlapping = db.query(Shift).filter(
        Shift.employee_id == shift.employee_id,
        Shift.shift_date == shift.shift_date,
        (
            (Shift.start_time <= shift.start_time) & (Shift.end_time > shift.start_time) |
            (Shift.start_time < shift.end_time) & (Shift.end_time >= shift.end_time) |
            (Shift.start_time >= shift.start_time) & (Shift.end_time <= shift.end_time)
        )
    ).first()
    
    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Shift overlaps with existing shift for this employee"
        )
    
    # Create new shift
    db_shift = Shift(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@router.get("/", response_model=list[Shift])
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
    query = db.query(Shift)
    
    if approved_only:
        query = query.filter(Shift.is_approved == True)
    
    if start_date:
        query = query.filter(Shift.shift_date >= start_date)
    
    if end_date:
        query = query.filter(Shift.shift_date <= end_date)
    
    if employee_id:
        query = query.filter(Shift.employee_id == employee_id)
    
    if branch_id:
        # Join with employees to filter by branch
        query = query.join(Employee).filter(Employee.branch_id == branch_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{shift_id}", response_model=Shift)
def read_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.shift_id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift

@router.put("/{shift_id}", response_model=Shift)
def update_shift(
    shift_id: int, 
    shift_update: ShiftCreate, 
    db: Session = Depends(get_db)
):
    db_shift = db.query(Shift).filter(Shift.shift_id == shift_id).first()
    if not db_shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    # Check if employee exists
    employee = db.query(Employee).filter(Employee.employee_id == shift_update.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check for overlapping shifts (excluding current shift)
    overlapping = db.query(Shift).filter(
        Shift.shift_id != shift_id,
        Shift.employee_id == shift_update.employee_id,
        Shift.shift_date == shift_update.shift_date,
        (
            (Shift.start_time <= shift_update.start_time) & (Shift.end_time > shift_update.start_time) |
            (Shift.start_time < shift_update.end_time) & (Shift.end_time >= shift_update.end_time) |
            (Shift.start_time >= shift_update.start_time) & (Shift.end_time <= shift_update.end_time)
        )
    ).first()
    
    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Shift overlaps with existing shift for this employee"
        )
    
    # Update fields
    for key, value in shift_update.dict().items():
        setattr(db_shift, key, value)
    
    db.commit()
    db.refresh(db_shift)
    return db_shift

@router.patch("/{shift_id}/approve", response_model=Shift)
def approve_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.shift_id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    shift.is_approved = True
    db.commit()
    db.refresh(shift)
    return shift

@router.delete("/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.shift_id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    db.delete(shift)
    db.commit()
    return {"message": "Shift deleted"}