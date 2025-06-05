from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import base
from .routes import branches, employees, shifts, auth

base.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(branches.router, prefix="/api/branches", tags=["branches"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(shifts.router, prefix="/api/shifts", tags=["shifts"])