# Biblioteca para envio de e-mail em formato http
import resend

# Constantes 
from app.constants import settings

class Email:
    """Classe para envio de e-mails usando a API Resend.

    Permite enviar e-mails HTML para destinatários específicos utilizando
    a chave de API e remetente definidos nas configurações da aplicação.

    Attributes:
        to_email (str): Endereço de e-mail do destinatário.
        _api_key_resend (str): Chave de API da Resend para autenticação.
        _sender (str): Endereço de e-mail ou nome do remetente.
    """

    def __init__(self, to_email: str):
        """Inicializa a classe Email com o destinatário.

        Args:
            to_email (str): Endereço de e-mail do destinatário.
        """
        self._api_key_resend = settings.API_KEY_RESEND
        self._sender = settings.SENDER
        self.to_email = to_email

    def send(self, subject: str, body: str) -> dict:
        """Envia um e-mail com assunto e corpo em HTML.

        Configura a chave de API, define remetente, destinatário, assunto
        e conteúdo HTML, e realiza o envio através da API Resend.

        Args:
            subject (str): Assunto do e-mail.
            body (str): Corpo do e-mail em HTML.

        Returns:
            dict: Resposta da API Resend contendo informações do envio.

        Raises:
            Exception: Se ocorrer algum erro externo durante o envio.
        """
        try:
            resend.api_key = self._api_key_resend

            params: resend.Emails.SendParams = {
                "from": f"HorizonTecnology <{self._sender}>",
                "to": [self.to_email],
                "subject": subject,
                "html": body, 
            } 
            email: resend.Emails.SendResponse = resend.Emails.send(params)
            return email
        except Exception as exc:
            raise Exception(f"Erro externo do servidor: {str(exc)}")
