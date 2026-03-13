from fastapi import status

"""
Módulo de Exceções Personalizadas – versão FastAPI

Define exceções específicas para tratamento de erros na aplicação,
incluindo recursos não encontrados, validação de dados, autenticação,
integridade de dados, sessão e limites de requisições.
"""

# =============================================================================
# EXCEÇÕES DE RECURSO / CONSULTA
# =============================================================================
class NotFoundError(Exception):
    """Erro quando um recurso solicitado não é encontrado.

    Attributes:
        status_code (int): Código HTTP 404.
    """
    status_code = status.HTTP_404_NOT_FOUND


class NotFoundFile(Exception):
    """Erro quando um arquivo solicitado não é encontrado.

    Attributes:
        status_code (int): Código HTTP 404.
    """
    status_code = status.HTTP_404_NOT_FOUND


# =============================================================================
# EXCEÇÕES DE VALIDAÇÃO DE DADOS
# =============================================================================
class EntityValidationError(Exception):
    """Falha de validação ao inserir ou atualizar dados de uma entidade.

    Attributes:
        status_code (int): Código HTTP 422.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class InvalidFieldsException(Exception):
    """Campos obrigatórios estão ausentes ou inválidos.

    Attributes:
        status_code (int): Código HTTP 422.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class UnprocessableEntity(Exception):
    """Erro de consistência ou semântica nos dados.

    Attributes:
        status_code (int): Código HTTP 422.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


# =============================================================================
# EXCEÇÕES DE AUTENTICAÇÃO / CREDENCIAIS
# =============================================================================
class InvalidCredentialsException(Exception):
    """Credenciais de autenticação inválidas.

    Attributes:
        status_code (int): Código HTTP 401.
    """
    status_code = status.HTTP_401_UNAUTHORIZED


# =============================================================================
# EXCEÇÕES DE INTEGRIDADE / DUPLICIDADE
# =============================================================================
class DuplicateReviewError(Exception):
    """Tentativa de inserir um registro duplicado.

    Attributes:
        status_code (int): Código HTTP 409.
    """
    status_code = status.HTTP_409_CONFLICT


class ForeignKeyReferenceError(Exception):
    """Falha de integridade referencial (chave estrangeira).

    Attributes:
        status_code (int): Código HTTP 409.
    """
    status_code = status.HTTP_409_CONFLICT


# =============================================================================
# EXCEÇÕES GENÉRICAS / DESCONHECIDAS
# =============================================================================
class UnknownError(Exception):
    """Erro não identificado – fallback genérico.

    Attributes:
        status_code (int): Código HTTP 500.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


# =============================================================================
# EXCEÇÕES DE SESSÃO
# =============================================================================
class SessionError(Exception):
    """Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.

    Attributes:
        status_code (int): Código HTTP 401.
    """
    status_code = status.HTTP_401_UNAUTHORIZED


# =============================================================================
# EXCEÇÃO DE LIMITE DE REQUISIÇÕES
# =============================================================================
class TooManyRequestsError(Exception):
    """Número de requisições excedido – limite de taxa atingido.

    Attributes:
        status_code (int): Código HTTP 429.
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# =============================================================================
# EXCEÇÃO DE EXPIRAÇÃO
# =============================================================================
class ExpirationError(Exception):
    """Recurso ou sessão expirada.

    Attributes:
        status_code (int): Código HTTP 401.
    """
    status_code = status.HTTP_401_UNAUTHORIZED


# =============================================================================
# EXCEÇÃO DE ROTA PROTEGIDA
# =============================================================================
class ProtectedRouteError(Exception):
    """Acesso a rota protegida sem permissão adequada.

    Attributes:
        status_code (int): Código HTTP 403.
    """
    status_code = status.HTTP_403_FORBIDDEN


# =============================================================================
# EXCEÇÃO DE AÇÃO PROIBIDA OU PROTEGIDA
# =============================================================================
class ForbiddenActionError(Exception):
    """Tentativa de realizar uma ação proibida ou protegida.

    Attributes:
        status_code (int): Código HTTP 403.
    """
    status_code = status.HTTP_403_FORBIDDEN
