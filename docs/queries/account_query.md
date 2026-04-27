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
           name 
            email 
            createdAt 
            updatedAt 
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
                "name": "Nome Usuário",
                "email": "usuario@email.com",
                "createdAt": 1775228778.306308,
                "updatedAt": 1776944662.517973
            }
        }
    }
}
```

##### Erro

```json
{
    "data": null,
    "errors": [
        {
            "message": "Mensagem de erro",
            "locations": [
                {
                    "line": 3,
                    "column": 9
                }
            ],
            "path": [
                "auth",
                "login"
            ],
            "extensions": {
                "typeError": "NomeDaExcecao",
                "statusCode": 401
            }
        }
    ]
}
```

#### Estrutura do retorno

| Campo | Tipo | Sempre presente | Descrição |
| --- | --- | --- | --- |
| `data` | `Resultado\| null` | Sim | Payload de sucesso da operação |

#### Estrutura de `error`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `message` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |


#### Exceções mapeadas

- `SessionError`: Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.
- `NotFoundError`: Erro quando um arquivo solicitado não é encontrado.
- `UnknownError`: Erro não identificado – fallback genérico.
