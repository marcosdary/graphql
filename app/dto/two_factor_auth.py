from pydantic import BaseModel, field_serializer
from datetime import datetime


class TwoFactorAuthModel(BaseModel):
    """
    Modelo de dados utilizado para autenticação de dois fatores (2FA).

    Este modelo representa as informações necessárias para um processo
    de 2FA, incluindo token, código numérico e data de expiração.

    Attributes:
        token (str): Token de verificação utilizado na autenticação de dois fatores.
        number (int): Código numérico enviado ao usuário para validação.
    """

    token: str
    number: int
