from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import User
from database import db, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/login", response_model=User)
def login(form_data: OAuth2PasswordRequestForm):
    username = form_data.username
    password = form_data.password

    user = db.query(User).filter_by(username=username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if not user.check_password(password):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    return user
