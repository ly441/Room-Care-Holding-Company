
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.auth_routes import router as auth_router
from app.routes.branches_routes import router as branches_router
from app.routes.employees_routes import router as employees_router
from app.routes.shifts_routes import router as shifts_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(branches_router, prefix="/api/branches", tags=["branches"])
app.include_router(employees_router, prefix="/api/employees", tags=["employees"])
app.include_router(shifts_router, prefix="/api/shifts", tags=["shifts"])
