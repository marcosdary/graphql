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


class RolesRouters(Enum):
    """Enumeração de rotas acessíveis por cada papel de usuário."""

    ADMIN = (
        "listUsers",
        "getAllPosts",
        "getByIdUser"
    )

    SUPER_ADMIN = (
        "listUsers",
        "createUserByAdmin",
        "createApiKey",
        "deleteUserByAdmin",
        "updateUserByAdmin",
        "deleteApiKey",
        "getByIdUser"
    )

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