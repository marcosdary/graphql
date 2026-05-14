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

    SESSION_EXPIRATION = 60 * 3
    TWO_FA_EXPIRATION = 5       # 10 minutos
    PASSWORD_RESET_EXPIRATION = 15 # 15 minutos

class Roles(Enum):
    """Enumeração de papéis de usuário."""

    user = "user"
    admin = "admin"
    super_admin = "super_admin"

class Papers(Enum):
    """Enumeração de papéis do token."""
    SESSION = "SESSION"
    API_KEY = "API_KEY"
