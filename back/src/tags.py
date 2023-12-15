from fastapi import APIRouter, HTTPException

from models import Tag, User
from database import Repository

router = APIRouter()


@router.get("/", response_model=list[Tag])
async def get_tags(user: User, repo: Repository):
    """Busca todas as tags de um usuário."""
    return await repo.get_tags(user.id)


@router.post("/", response_model=Tag)
async def add_tag(tag: Tag, user: User, repo: Repository):
    """Adiciona uma tag para um usuário."""
    tag.user_id = user.id
    await repo.add_tag(tag)
    return tag


@router.put("/", response_model=Tag)
async def edit_tag(tag: Tag, user: User, repo: Repository):
    """Atualiza uma tag."""
    tag.user_id = user.id
    await repo.update_tag(tag)
    return tag


@router.delete("/", response_model=None)
async def delete_tag(id: int, user: User, repo: Repository):
    """Exclui uma tag."""
    tag = await repo.get_tags(user.id, id=id)

    if not tag:
        raise HTTPException(status_code=404, detail="Tag não encontrada")

    await repo.delete_tag(tag.id)
    return None

