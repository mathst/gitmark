from fastapi import APIRouter, HTTPException

from models import Tag,User
from database import db

router = APIRouter()

@router.get("/", response_model=list[Tag])
def get_tags(user: User):
    return db.query(Tag).filter_by(user_id=user.id).all()

@router.post("/", response_model=Tag)
def add_tag(tag: Tag, user: User):
    tag.user_id = user.id
    db.add(tag)
    db.commit()
    return tag

@router.put("/", response_model=Tag)
def edit_tag(tag: Tag, user: User):
    tag.user_id = user.id
    db.update(tag)
    db.commit()
    return tag

@router.delete("/", response_model=None)
def delete_tag(id: int, user: User):
    tag = db.query(Tag).filter_by(id=id, user_id=user.id).first()

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")

    db.delete(tag)
    db.commit()
    return None
