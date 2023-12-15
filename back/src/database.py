import asyncio
import sqlalchemy as sa
from models import User,Tag
from sqlalchemy.ext.asyncio import create_async_engine

def init_database(database_url):
    """Inicializa o banco de dados."""
    engine = create_async_engine(database_url)
    Base = sa.declarative_base()
    Base.metadata.create_all(engine)

class Database:
    """Representa a conexão com o banco de dados."""

    def __init__(self, database_url):
        self.engine = create_async_engine(database_url)

    async def init_database(self):
        """Inicializa o banco de dados."""
        self.Base = sa.declarative_base()
        self.Base.metadata.create_all(self.engine)

    async def get_database(self):
        """Retorna uma conexão com o banco de dados."""
        return await self.engine.connect()

    async def close_database(self):
        """Fecha o banco de dados."""
        await self.engine.close()


class Repository:
    """Representa as operações de acesso ao banco de dados."""

    def __init__(self, database: Database):
        self.database = database

    async def get_users(self):
        query = """
            SELECT *
            FROM users
        """
        result = await self.database.execute(query)
        return [User(**row) for row in result]

    async def add_user(self, user: User):
        query = """
            INSERT INTO users (username, password)
            VALUES (:username, :password)
        """
        await self.database.execute(query, {"username": user.username, "password": user.password})

    async def edit_user(self, user: User):
        query = """
            UPDATE users
            SET username = :username,
                password = :password
            WHERE id = :id
        """
        await self.database.execute(query, {"username": user.username, "password": user.password, "id": user.id})

    async def delete_user(self, user_id: int):
        query = """
            DELETE FROM users
            WHERE id = :id
        """
        await self.database.execute(query, {"id": user_id})
    
    async def get_user_by_username(self, username):
        """Busca um usuário por nome de usuário."""
        async with self.database.get_database() as connection:
            query = """
                SELECT *
                FROM users
                WHERE username = :username
            """
            result = await connection.execute(query, {"username": username})
            return result.first()

    async def get_tags(self):
        """Busca todas as tags."""
        async with self.database.get_database() as connection:
            query = """
                SELECT *
                FROM tags
            """
            result = await connection.execute(query)
            return result.fetchall()

    async def add_user(self, user: User):
        """Adiciona um usuário."""
        async with self.database.get_database() as connection:
            query = """
                INSERT INTO users (username, password)
                VALUES (:username, :password)
            """
            await connection.execute(query, {"username": user.username, "password": user.password})

    async def update_user(self, user: User):
        """Atualiza um usuário."""
        async with self.database.get_database() as connection:
            query = """
                UPDATE users
                SET username = :username,
                    password = :password
                WHERE id = :id
            """
            await connection.execute(query, {"username": user.username, "password": user.password, "id": user.id})

    async def delete_user(self, user_id: int):
        """Exclui um usuário."""
        async with self.database.get_database() as connection:
            query = """
                DELETE FROM users
                WHERE id = :id
            """
            await connection.execute(query, {"id": user_id})


class User:
    """Representa um usuário."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User username={self.username} password={self.password}>"

class Tags:
    """Representa as tags do usuario"""
    
    async def get_tags(self, user_id: int):
        """Busca todas as tags de um usuário."""
        async with self.database.get_database() as connection:
            query = """
                SELECT *
                FROM tags
                WHERE user_id = :user_id
            """
            result = await connection.execute(query, {"user_id": user_id})
            return result.fetchall()

    async def add_tag(self, tag: Tag):
        """Adiciona uma tag para um usuário."""
        async with self.database.get_database() as connection:
            query = """
                INSERT INTO tags (name, user_id)
                VALUES (:name, :user_id)
            """
            await connection.execute(query, {"name": tag.name, "user_id": tag.user_id})

    async def update_tag(self, tag: Tag):
        """Atualiza uma tag."""
        async with self.database.get_database() as connection:
            query = """
                UPDATE tags
                SET name = :name
                WHERE id = :id
            """
            await connection.execute(query, {"name": tag.name, "id": tag.id})
            

    async def delete_tag(self, id: int):
        """Exclui uma tag."""
        async with self.database.get_database() as connection:
            query = """
                DELETE FROM tags
                WHERE id = :id
            """
            await connection.execute(query, {"id": id})

