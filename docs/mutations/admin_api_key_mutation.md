# API Key Mutation

Documentação representa para registrar no API KEY para acessar a API.

## Visão geral

- Tipo de operacao: `mutation`
- Objetivo: tem a responsabilidade de registrar novas chaves de API.

## Regras de acesso

| Operação | Tipo | Acesso | Permissões | Observações |
| --- | --- | --- | --- | --- |
| `create` | `mutation` | Protegido | `[SessionPermission, RolePermission]` | Regras resumidas de autenticação/autorizacção |
| `delete` | `mutation` | Protegido | `[SessionPermission, RolePermission]` | Regras resumidas de autenticação |

## Operações

<!--Criar API Key-->
### `create`

#### Resumo

Objetivo é criar API KEY no sistema, para que tenha acesso as funcionalidades
baseado em seu papel.

#### Assinatura do GraphQL

```graphql
mutation CreateApiKey($schema: ApiKeyInput!){
    admin {
        apiKey {
            create (schema: $schema) {
                token
                expiresAt
            }
        }
    }
}
```
#### Variáveis

```json
{
    "schema": {
        "expiration": "EXPIRATION"
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório | Tipo | Exemplo | 
| --- | --- | --- | --- | 
| `Authorization` | Sim | Bearer token | `"Bearer eyJhbGciOiJIUz...."` |


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `expiration` | `String` | Sim | parâmetro direto | Expiração da API Key | `"SEVEN_DAYS"` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "admin": {
            "apiKey": {
                "create": {
                    "token": "eyJhbGciO...",
                    "expiresAt": 1777571494.790612
                }
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

#### Estrutura de `errors`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `message` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |


#### Exceções mapeadas

- `UnknownError`: Erro não identificado – fallback genérico.

<!--Deletar API Key-->
### `delete`

#### Resumo

Objetivo é deleyar API KEY do sistema.

#### Assinatura do GraphQL

```graphql
mutation DeleteApiKeySchema($key: String!){
    admin {
        apiKey {
            delete(key: $key) {
                success
                data 
                error { errorName typeError statusCode }
            }
        }
    }
}
```
#### Variáveis

```json
{
    "key": "eyJhbGci..."
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório | Tipo | Exemplo | 
| --- | --- | --- | --- | 
| `X-Api-Key` | Sim | String | `"eyJhbGciOiJIUz...."` |
| `Authorization` | Sim | Bearer token | `"Bearer eyJhbGciOiJIUz...."` |


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `key` | `String` | Sim | parâmetro direto | Chave da API Key | `"eyJhbGci..."` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "admin": {
            "apiKey": {
                "delete": null
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

#### Estrutura de `errors`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `message` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |


#### Exceções mapeadas

- `UnknownError`: Erro não identificado – fallback genérico.
- `ExpirationError`: Recurso ou sessão expirada.