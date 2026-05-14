from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

# Model
from app.models import RolePermissions

# Exceptions
from app.exceptions import (
    NotFoundError,
)


class RolePermissionsRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, role_id: str, permission_id: str) -> RolePermissions:
        model = RolePermissions(role_id=role_id, permission_id=permission_id)
        self.session.add(model)
        return model
    
    async def list_permissions_by_role(self, role_id: str) -> List[RolePermissions]:  
        query = select(RolePermissions).where(RolePermissions.role_id == role_id)
        list_query = query.order_by(RolePermissions.created_at.desc())        
        stmt = await self.session.scalars(
            list_query
        )
        rows = stmt     
        return rows
    
    async def list_roles_by_permission(self, permission_id: str) -> List[RolePermissions]:  
        query = select(RolePermissions).where(RolePermissions.permission_id == permission_id)
        list_query = query.order_by(RolePermissions.created_at.desc())        
        stmt = await self.session.scalars(
            list_query
        )
        rows = stmt     
        return rows

    async def delete(self, role_id: str, permission_id: str) -> None:
        
        row = await self.session.scalar(
            select(RolePermissions).where(RolePermissions.role_id == role_id, RolePermissions.permission_id == permission_id)
        )

        if not row:
            raise NotFoundError("Conteúdo não encontrada.")

        await self.session.delete(row)
