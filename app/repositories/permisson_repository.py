from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

# Model
from app.models import Permission

# DTOs
from app.dto.permission import (
    PermissionCreate,
)

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
)


class PermissionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, schemas: PermissionCreate) -> Permission: 
        models = []
        for line in schemas: 
            models.append(Permission(**line.model_dump()))

        self.session.add_all(models)
        return models
    
    async def get_permission_by_id(self, permission_id: str) -> Permission:
       

        permission = await self.session.scalar(
            select(Permission).where(Permission.permission_id == permission_id)
        )
            
        if not permission:
            raise NotFoundError("Permissão não encontrado.")

        return permission
        
        
    async def list_permissions(self) -> List[Permission]:
       
        query = select(Permission)

        list_query = query.order_by(Permission.created_at.desc())
            
        stmt = await self.session.scalars(
            list_query
        )

        rows = stmt
            
        return rows


    async def delete_permission(self, permission_id: str) -> None:
        
        permission = await self.session.scalar(
            select(Permission).where(Permission.permission_id == permission_id)
        )

        if not permission:
            raise NotFoundError("Permissão não encontrada.")

        await self.session.delete(permission)
