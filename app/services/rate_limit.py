from app.constants import redisClient
from app.exceptions import TooManyRequestsError

def check_rate_limit(ipUser: str) -> None:
    """Verifica se um usuário excedeu o limite de requisições por minuto.

    Utiliza Redis para armazenar o contador de requisições por IP.
    Se o limite for atingido, levanta uma exceção `TooManyRequestsError`.

    Args:
        ipUser (str): Endereço IP do usuário que está fazendo a requisição.

    Raises:
        TooManyRequestsError: Se o usuário exceder 10 requisições por minuto.
    """
    key = f"rate:{ipUser}"
    current = redisClient.incr(key)
    if current == 1:
        redisClient.expire(key, 60)

    if current >= 11:
        raise TooManyRequestsError("Acesso negado. Tentativas excessivas")
