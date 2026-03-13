from abc import ABC, abstractmethod

class Template(ABC):
    """Classe abstrata base para templates de e-mail.

    Define a interface que todos os templates de e-mail devem implementar,
    garantindo que cada template forneça o HTML completo através da propriedade `get_template`.
    """

    @property
    @abstractmethod
    def get_template(self) -> str:
        """Retorna o conteúdo HTML do template de e-mail.

        Returns:
            str: HTML do e-mail pronto para envio.
        """
        ...

class GeralActionTemplate(Template):
    """Template de e-mail genérico para ações do usuário, como códigos temporários.

    Gera um HTML estruturado com título, cabeçalho, código de ação e tempo de expiração.

    Attributes:
        _title (str): Título do e-mail.
        _header (str): Cabeçalho do e-mail.
        _number (int): Código numérico enviado ao usuário.
        _expiresAt (str): Prazo de expiração do código.
    """

    def __init__(self, title: str, header: str, number: int, expiresAt: str):
        self._title = title
        self._header = header
        self._number = number
        self._expiresAt = expiresAt

    @property
    def get_template(self) -> str:
        """Retorna o HTML formatado do e-mail.

        Returns:
            str: HTML completo com estilo inline, código e tempo de expiração.
        """
        return f"""
    <!DOCTYPE html>
    <html>
        <head>
        <meta charset="UTF-8">
        <title>{self._title}</title>
        </head>
        <body style="margin:0; padding:0; background-color:#f4f4f4; font-family:Arial, Helvetica, sans-serif;">

            <table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4">
            <tr>
                <td align="center">

                <table width="600" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="margin:40px 0; border-radius:8px;">
                    
                    <!-- Cabeçalho -->
                    <tr>
                    <td align="center" bgcolor="#4e73df" style="padding:30px; border-radius:8px 8px 0 0;">
                        <h1 style="color:#ffffff; margin:0; font-size:24px;">
                        {self._header}
                        </h1>
                    </td>
                    </tr>

                    <!-- Conteúdo -->
                    <tr>
                    <td align="center" style="padding:40px 30px;">
                        <p style="font-size:16px; color:#333333; margin:0 0 20px 0;">
                        Use o código abaixo para concluir seu acesso:
                        </p>

                        <!-- Código -->
                        <table cellpadding="0" cellspacing="0">
                        <tr>
                            <td align="center" style="font-size:32px; letter-spacing:8px; font-weight:bold; color:#4e73df; padding:15px 25px; border:2px dashed #4e73df; border-radius:6px;">
                            {self._number}
                            </td>
                        </tr>
                        </table>

                        <p style="font-size:14px; color:#777777; margin:25px 0 0 0;">
                        Este código expira em {self._expiresAt}.
                        </p>
                    </td>
                    </tr>

                    <!-- Rodapé -->
                    <tr>
                    <td align="center" style="padding:20px; font-size:12px; color:#999999;">
                        Se você não solicitou este código, ignore este e-mail.
                    </td>
                    </tr>

                </table>

                </td>
            </tr>
            </table>

        </body>
    </html>
    """

class AdminNowTemplate(Template):
    """Template de e-mail para criação de usuário administrador.

    Gera um HTML estruturado com título, cabeçalho e credenciais do novo administrador.

    Attributes:
        _title (str): Título do e-mail.
        _header (str): Cabeçalho do e-mail.
        _name (str): Nome do administrador.
        _email (str): E-mail do administrador.
        _password (str): Senha temporária do administrador.
    """

    def __init__(self, title: str, header: str, name: str, email: str, password: str):
        self._title = title
        self._header = header
        self._name = name
        self._email = email
        self._password = password

    @property
    def get_template(self) -> str:
        """Retorna o HTML formatado do e-mail com credenciais do administrador.

        Returns:
            str: HTML completo incluindo nome, e-mail e senha temporária.
        """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <title>{self._title}</title>
        </head>

        <body style="margin:0; padding:0; background-color:#f4f4f4; font-family:Arial, Helvetica, sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4">
        <tr>
        <td align="center">

        <table width="600" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="margin:40px 0; border-radius:8px;">

            <!-- Cabeçalho -->
            <tr>
            <td align="center" bgcolor="#4e73df" style="padding:30px; border-radius:8px 8px 0 0;">
                <h1 style="color:#ffffff; margin:0; font-size:24px;">
                {self._header}
                </h1>
            </td>
            </tr>

            <!-- Conteúdo -->
            <tr>
            <td style="padding:40px 30px; color:#333333;">

                <p style="font-size:16px; margin:0 0 20px 0;">
                Olá <strong>{self._name}</strong>,
                </p>

                <p style="font-size:16px; margin:0 0 20px 0;">
                Seu acesso ao sistema foi criado com sucesso. Utilize as credenciais abaixo para realizar o primeiro login:
                </p>

                <!-- Credenciais -->
                <table width="100%" cellpadding="0" cellspacing="0" style="margin:25px 0;">
                    <tr>
                        <td style="padding:15px; border:1px solid #e3e3e3; border-radius:6px;">

                            <p style="margin:0 0 10px 0; font-size:14px;">
                                <strong>E-mail:</strong> {self._email}
                            </p>

                            <p style="margin:0; font-size:14px;">
                                <strong>Senha:</strong> {self._password}
                            </p>

                        </td>
                    </tr>
                </table>

                <p style="font-size:13px; color:#777777; margin-top:30px;">
                Por segurança, recomendamos que você altere sua senha após o primeiro acesso.
                </p>

            </td>
            </tr>

            <!-- Rodapé -->
            <tr>
            <td align="center" style="padding:20px; font-size:12px; color:#999999;">
                Caso você não reconheça este cadastro, ignore este e-mail.
            </td>
            </tr>

        </table>

        </td>
        </tr>
        </table>

        </body>
        </html>
        """