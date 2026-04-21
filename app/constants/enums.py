from enum import Enum


class ExpirationApiKey(Enum):
    """Enumeração de períodos de expiração para chaves de API."""

    ONE_HOUR = 60 * 60
    ONE_DAY = 1 * 24 * 60 * 60
    TWO_DAYS = 2 * 24 * 60 * 60
    SEVEN_DAYS = 7 * 24 * 60 * 60
    THIRTY_DAYS = 30 * 24 * 60 * 60
    NINETY_DAYS = 90 * 24 * 60 * 60
    ONE_YEAR = 365 * 24 * 60 * 60


class ExpirationTimes(Enum):
    """Enumeração de tempos de expiração para sessões e tokens."""

    SESSION_EXPIRATION = 10_800  # 3 horas
    TWO_FA_EXPIRATION = 600       # 10 minutos
    PASSWORD_RESET_EXPIRATION = 900  # 15 minutos

class Permissions(Enum):
    """Permissões atômicas por domínio."""

    # Usuários
    LIST_USERS         = "listUsers"
    GET_USER_BY_ID     = "getByIdUser"
    CREATE_USER        = "createUserByAdmin"
    UPDATE_USER        = "updateUserByAdmin"
    DELETE_USER        = "deleteUserByAdmin"
    CREATE             = "create"
    LOGIN              = "login"
    VERIFY_TWO_FACTOR  = "verifyTwoFactor" 
    FORGOT_PASSWORD    = "forgotPassword"
    RESET_PASSWORD     = "resetPassword"
    UPDATE             = "update"
    DELETE             = "delete"
    GET_USER           = "getUser"


    # API Keys
    CREATE_API_KEY     = "createApiKey"
    DELETE_API_KEY     = "deleteApiKey"

# Permissões base — building blocks
BASE_PERMISSIONS = frozenset()

USER_PERMISSIONS = frozenset({
    Permissions.CREATE,
    Permissions.LOGIN,
    Permissions.RESET_PASSWORD,
    Permissions.VERIFY_TWO_FACTOR,
    Permissions.FORGOT_PASSWORD,
    Permissions.UPDATE,
    Permissions.DELETE,
    Permissions.GET_USER
})

ADMIN_PERMISSIONS = USER_PERMISSIONS | frozenset({
    Permissions.LIST_USERS,
    Permissions.GET_USER_BY_ID,
})

SUPER_ADMIN_PERMISSIONS =  ADMIN_PERMISSIONS | frozenset({
    Permissions.CREATE_USER,
    Permissions.UPDATE_USER,
    Permissions.DELETE_USER,
    Permissions.CREATE_API_KEY,
    Permissions.DELETE_API_KEY,
})

class RolePermissions(Enum):
    ADMIN       = ADMIN_PERMISSIONS
    SUPER_ADMIN = SUPER_ADMIN_PERMISSIONS
    USER = USER_PERMISSIONS

    def has_permissions(self, permission: Permissions) -> bool:
        permission = Permissions(permission)
        return permission in self.value

class Roles(Enum):
    """Enumeração de papéis de usuário."""

    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class SendType(Enum):
    REGISTER = "REGISTER"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    TWO_FACTOR_AUTH = "TWO_FACTOR_AUTH"
    PASSWORD_RESET = "PASSWORD_RESET"

class ExpirationAt(Enum):
    TEN_MINUTES     = "TEN_MINUTES"
    FIFTEEN_MINUTES = "FIFTEEN_MINUTES"
    TWENTY_MINUTES  = "TWENTY_MINUTES"
    ONE_HOUR        = "ONE_HOUR"