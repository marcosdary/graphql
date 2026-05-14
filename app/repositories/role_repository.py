from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

# Model
from app.models import Role

# DTOs
from app.dto.role import (
    RoleCreate,
)

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
)


class RoleRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, schemas: List[RoleCreate]) -> List[Role]:
        models = []
        for line in schemas: 
            models.append(Role(**line.model_dump()))

        self.session.add_all(models)
        return models
    
            
    async def get_role_by_id(self, role_id: str) -> Role: 

        role = await self.session.scalar(
            select(Role).where(Role.role_id == role_id)
        )
            
        if not role:
            raise NotFoundError("Role não encontrado.")

        return role
    
    async def get_role_by_name(self, name: str) -> str: 

        role_id = await self.session.scalar(
            select(Role.role_id).where(Role.name == name)
        )
            
        if not role_id:
            raise NotFoundError("Role não encontrado.")

        return role_id
        
        
    async def list_role(self) -> List[Role]:
       
        query = select(Role)

        list_query = query.order_by(Role.created_at.desc())
            
        stmt = await self.session.scalars(
            list_query
        )

        rows = stmt
            
        return rows


    async def delete_role(self, role_id: str) -> None:
        
        role = await self.session.scalar(
            select(Role).where(Role.role_id == role_id)
        )

        if not role:
            raise NotFoundError("Role não encontrada.")

        await self.session.delete(role)
