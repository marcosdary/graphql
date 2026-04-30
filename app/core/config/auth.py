from bcrypt import hashpw, checkpw, gensalt
import hmac
import hashlib

from app.core.config.settings import settings

class Auth:
    """Classe utilitária para hash e verificação de senhas usando bcrypt.

    Fornece métodos para gerar hashes seguros de senhas e verificar
    se uma senha em texto plano corresponde ao hash armazenado.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera um hash seguro para a senha fornecida.

        Args:
            password (str): Senha em texto plano que será criptografada.

        Returns:
            str: Hash da senha codificado em UTF-8.
        """
        return hashpw(password.encode(), gensalt()).decode()
    
    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verifica se uma senha em texto plano corresponde ao hash fornecido.

        Args:
            plain (str): Senha em texto plano a ser verificada.
            hashed (str): Hash da senha armazenado.

        Returns:
            bool: True se a senha corresponde ao hash, False caso contrário.
        """
        return checkpw(plain.encode(), hashed.encode())

    @staticmethod
    def hash_code(code: str) -> str:
        return hmac.new(
            settings.TWO_FACTOR_AUTH_KEY.encode(),
            code.encode(),
            hashlib.sha256
        ).hexdigest()
    

    @staticmethod
    def verify_code(code: str, code_hash: str) -> bool:
        hash_compare = Auth.hash_code(code)
        return hmac.compare_digest(hash_compare, code_hash)
    
