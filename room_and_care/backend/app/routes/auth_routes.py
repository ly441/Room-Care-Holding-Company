from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.schemas.schemas import Token, EmployeeCreate
from app.utils import auth  

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.get_password_hash(employee.password)
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        role=employee.role,
        hourly_rate=employee.hourly_rate,
        hire_date=employee.hire_date,
        email=employee.email,
        hashed_password=hashed_password,
        branch_id=1  # Default branch
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return {"message": "User created successfully"}
