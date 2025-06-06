from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.branch import Branch
from app.schemas.schemas import BranchCreate, Branch

router = APIRouter()

@router.post("/", response_model=Branch)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    db_branch = Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

@router.get("/", response_model=list[Branch])
def read_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Branch).offset(skip).limit(limit).all()

@router.get("/{branch_id}", response_model=Branch)
def read_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

@router.put("/{branch_id}", response_model=Branch)
def update_branch(branch_id: int, branch: BranchCreate, db: Session = Depends(get_db)):
    db_branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not db_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    for key, value in branch.dict().items():
        setattr(db_branch, key, value)
    db.commit()
    db.refresh(db_branch)
    return db_branch

@router.delete("/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    db.delete(branch)
    db.commit()
    return {"message": "Branch deleted"}