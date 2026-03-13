from bcrypt import hashpw, checkpw, gensalt

class HashPassword:
    """Classe utilitária para hash e verificação de senhas usando bcrypt.

    Fornece métodos para gerar hashes seguros de senhas e verificar
    se uma senha em texto plano corresponde ao hash armazenado.
    """

    def hash_password(self, password: str) -> str:
        """Gera um hash seguro para a senha fornecida.

        Args:
            password (str): Senha em texto plano que será criptografada.

        Returns:
            str: Hash da senha codificado em UTF-8.
        """
        return hashpw(password.encode(), gensalt()).decode()

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verifica se uma senha em texto plano corresponde ao hash fornecido.

        Args:
            plain (str): Senha em texto plano a ser verificada.
            hashed (str): Hash da senha armazenado.

        Returns:
            bool: True se a senha corresponde ao hash, False caso contrário.
        """
        return checkpw(plain.encode(), hashed.encode())
