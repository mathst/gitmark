from fastapi import APIRouter, HTTPException

from models import Repository,User
from database import db

router = APIRouter()

@router.get("/", response_model=list[Repository])
def get_repositories(user: User):
    return db.query(Repository).filter_by(user_id=user.id).all()
