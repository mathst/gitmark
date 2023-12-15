from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_database, get_database, close_database
from models import User, Repository, Tag

from auth import auth_router
from repositories import repositories_router
from tags import tags_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Inicializa o banco de dados na inicialização do aplicativo."""
    await init_database()


@app.on_event("shutdown")
async def shutdown():
    """Fecha o banco de dados no encerramento do aplicativo."""
    await close_database()

app.include_router(auth_router)
app.include_router(repositories_router)
app.include_router(tags_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
