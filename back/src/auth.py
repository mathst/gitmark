from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models import User

router = APIRouter()


@router.post("/login", response_model=User)
async def login(
    form_data: OAuth2PasswordRequestForm,
    repository: Repository,
):
    """Autentica um usuário."""
    username = form_data.username
    password = form_data.password

    user = await repository.get_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if not user.check_password(password):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    return user


@router.get("/", response_model=list[User])
async def get_users(user: User):
    return await repository.get_users()


@router.post("/", response_model=User)
async def add_user(user: User):
    return await repository.add_user(user)


@router.put("/", response_model=User)
async def edit_user(user: User):
    return await repository.edit_user(user)


@router.delete("/", response_model=None)
async def delete_user(user: User):
    await repository.delete_user(user.id)
    return None