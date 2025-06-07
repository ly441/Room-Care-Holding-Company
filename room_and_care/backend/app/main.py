from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from  app.database import engine
from  app.database import Base
from  app.routes.branches_routes import Branch
from  app.routes.employees_routes import Employee
from  app.routes.shifts_routes import Shift
from  app.utils.auth import APIRouter

Base.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(APIRouter.router, prefix="/api/auth", tags=["auth"])
app.include_router(Branch.router, prefix="/api/branches", tags=["branches"])
app.include_router(Employee.router, prefix="/api/employees", tags=["employees"])
app.include_router(Shift.router, prefix="/api/shifts", tags=["shifts"])