
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.branch import Branch as BranchModel
from app.schemas.schemas import BranchCreate, Branch as BranchSchema

router = APIRouter()

@router.post("/", response_model=BranchSchema)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    db_branch = BranchModel(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

@router.get("/", response_model=List[BranchSchema])
def read_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(BranchModel).offset(skip).limit(limit).all()

@router.get("/{branch_id}", response_model=BranchSchema)
def read_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(BranchModel).filter(BranchModel.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

@router.put("/{branch_id}", response_model=BranchSchema)
def update_branch(branch_id: int, branch: BranchCreate, db: Session = Depends(get_db)):
    db_branch = db.query(BranchModel).filter(BranchModel.branch_id == branch_id).first()
    if not db_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    for key, value in branch.dict().items():
        setattr(db_branch, key, value)
    db.commit()
    db.refresh(db_branch)
    return db_branch

@router.delete("/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(BranchModel).filter(BranchModel.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    db.delete(branch)
    db.commit()
    return {"message": "Branch deleted"}
