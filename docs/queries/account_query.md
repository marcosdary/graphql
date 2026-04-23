# Account Query

Documentação representa o acesso às informações do usuário

## Visão geral

- Tipo de operacao: `query`
- Objetivo: tem a responsabilidade de autenticar o usuário

## Regras de acesso

| Operação | Tipo | Acesso | Permissões | Observações |
| --- | --- | --- | --- | --- |
| `me` | `query` | Público | `[ApiKeyPermission, SessionPermission]` | Regras resumidas de autenticação/autorizacção |


## Operações

<!--Informações-->
### `me`

#### Resumo

Objetivo do me é acessar informações do usuário no sistema.

#### Assinatura do GraphQL

```graphql
query {
    user {
        me {
            success
            data { 
                name 
                email 
                createdAt 
                updatedAt 
            }
            error { errorName typeError statusCode }
            timestamp
        }
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório | Tipo | Exemplo | 
| --- | --- | --- | --- | 
| `X-Api-Key` | Sim | String | `"eyJhbGciOiJIUz...."` |
| `Authorization` | Sim | Bearer token | `"Bearer eyJhbGciOiJIUz...."` |


#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "user": {
            "me": {
                "success": true,
                "data": {
                    "name": "Nome Usuário",
                    "email": "usuario@email.com",
                    "createdAt": 1775228778.306308,
                    "updatedAt": 1776944662.517973
                },
                "error": null,
                "timestamp": 1776946703.395913
            }
        }
    }
}
```

##### Erro

```json
{
    "data": {
        "auth": {
            "me": {
                "success": false,
                "data": null,
                "error": {
                    "errorName": "Mensagem de erro",
                    "typeError": "NomeDaExcecao",
                    "statusCode": 401
                },
                "timestamp": 0
            }
        }
    }
}
```

#### Estrutura do retorno

| Campo | Tipo | Sempre presente | Descrição |
| --- | --- | --- | --- |
| `success` | `bool` | Sim | Indica se a operacao foi concluida com sucesso |
| `data` | `Resultado\| null` | Sim | Payload de sucesso da operação |
| `error` | `ApiErrorType \| null` | Sim | Payload de erro quando `success=false` |
| `timestamp` | `datetime` | Sim | Data e hora em que `build_response` montou a resposta |

#### Estrutura de `error`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `errorName` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |


#### Exceções mapeadas

- `SessionError`: Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.
- `NotFoundError`: Erro quando um arquivo solicitado não é encontrado.
- `UnknownError`: Erro não identificado – fallback genérico.
