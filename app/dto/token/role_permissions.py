from pydantic import BaseModel, ConfigDict

from app.dto.role import RoleRead
from app.dto.permission import PermissionRead

class RolePermissions(BaseModel):
    """
    Modelo base para usuários, utilizado como superclasse para outros modelos de usuário.

    Este modelo configura o Pydantic para aceitar atributos diretamente de objetos,
    facilitando a conversão de objetos para modelos Pydantic.

    Attributes:
        model_config (ConfigDict): Configuração do Pydantic que permite criar
            instâncias do modelo a partir de atributos de objetos.
    """

    role: RoleRead
    permission: PermissionRead

    model_config = ConfigDict(from_attributes=True)