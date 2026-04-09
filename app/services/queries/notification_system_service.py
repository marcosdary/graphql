from app.clients import NotificationSystemClient
from app.dto.notification_system import (
    NotificationSystemReadModel,
    NotificationSystemCreateModel
)
from app.constants import ExpirationAt, SendType
from app.exceptions import ApiError

class NotificationSystemService:

    def __init__(self):
        self._notification_system_client = NotificationSystemClient()

    async def select_by_id(self, id_email: str) -> dict: 
        query = """
            query EmailNotificationSchema($idEmail: String!) {
                selectById(idEmail: $idEmail) {
                    success
                    data {
                        idEmail
                        recipientEmail
                        sendType
                        status
                        providerResponse
                        createdAt
                        processedAt
                    }
                    error { errorName typeError statusCode }
                }
            }
        """
        variables = {"idEmail": id_email}
        return await self._notification_system_client.execute_request(
            query=query, 
            variables=variables
        )
    
    async def select_all(self) -> dict:
        query = """
            query {
                select_all: selectAll {
                    success
                    data {
                        idEmail
                        recipientEmail
                        sendType
                        status
                        providerResponse
                        createdAt
                        processedAt
                    }
                    error { errorName typeError statusCode }
                }
            }
        """

        return await self._notification_system_client.execute_request(
            query=query
        )
    
    async def delete(self, id_email: str) -> dict:
        query = """
            mutation EmailNotificationSchema($idEmail: String!) {
                delete(idEmail: $idEmail){
                    success
                    data {
                        idEmail
                        recipientEmail
                        sendType
                        status
                        providerResponse
                        createdAt
                        processedAt
                    }
                    error { errorName typeError statusCode }
                }
            }
        """
        variables = {"idEmail": id_email}
        return await self._notification_system_client.execute_request(
            query=query,
            variables=variables
        )
    
    async def create(self, schema: NotificationSystemCreateModel) -> NotificationSystemReadModel:
        query = """
            mutation EmailNotificationSchema($schema: EmailNotificationInput!) {
                create(schema: $schema){
                    success
                    data {
                        idEmail
                        recipientEmail
                        sendType
                        status
                        providerResponse
                        createdAt
                        processedAt
                    }
                    error { errorName typeError statusCode }
                }
            }
        """
        variables = {
            "schema": schema.model_dump(mode="json")
        }

        response = await self._notification_system_client.execute_request(
            query=query,
            variables=variables
        )

        data: dict = response["data"]

        if not data.get("create"):
            raise ApiError("Erro de envio para servidor externo")

        response_create: dict = data.get("create")

        if not response_create.get("success"):
            response_error: dict = response_create.get("error")
            raise ApiError(f"Erro servidor externo: {response_error.get("nameError")}")
        
        return NotificationSystemReadModel.model_validate(response_create.get("data"))


    