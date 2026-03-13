from pydantic import BaseModel


class ApiErrorModel(BaseModel):
    """
    Modelo de resposta de erro para APIs.

    Este modelo é utilizado para padronizar a estrutura de erros
    retornados pela API, incluindo nome do erro, tipo e código HTTP.

    Attributes:
        errorName (str): Nome ou descrição do erro ocorrido.
        typeError (str): Tipo ou categoria do erro (ex: "ValidationError").
        statusCode (int | None): Código HTTP associado ao erro. Pode ser None
            se não houver código específico definido.
    """

    errorName: str
    typeError: str
    statusCode: int | None = None