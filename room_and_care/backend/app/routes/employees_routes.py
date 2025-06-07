
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.employee import Employee as EmployeeModel
from app.schemas.schemas import EmployeeCreate, Employee  # Pydantic schemas

router = APIRouter()


@router.post("/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing_employee = db.query(EmployeeModel).filter(EmployeeModel.email == employee.email).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_employee = EmployeeModel(
        first_name=employee.first_name,
        last_name=employee.last_name,
        role=employee.role,
        hourly_rate=employee.hourly_rate,
        hire_date=employee.hire_date,
        email=employee.email,
        branch_id=employee.branch_id,
        is_active=True
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/", response_model=List[Employee])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    branch_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EmployeeModel)

    if active_only:
        query = query.filter(EmployeeModel.is_active == True)

    if branch_id:
        query = query.filter(EmployeeModel.branch_id == branch_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: int,
    employee_update: EmployeeCreate,
    db: Session = Depends(get_db)
):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if employee_update.email != db_employee.email:
        existing_employee = db.query(EmployeeModel).filter(
            EmployeeModel.email == employee_update.email,
            EmployeeModel.employee_id != employee_id
        ).first()
        if existing_employee:
            raise HTTPException(status_code=400, detail="Email already in use by another employee")

    for key, value in employee_update.dict().items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.patch("/{employee_id}/status", response_model=Employee)
def update_employee_status(
    employee_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db_employee.is_active = is_active
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Soft delete (mark as inactive)
    employee.is_active = False
    db.commit()
    return {"message": "Employee deactivated"}
