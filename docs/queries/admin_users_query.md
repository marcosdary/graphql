# Account Query

Documentação representa o acesso às informações dos usuários por meio do administrador (ADMIN ou SUPER_ADMIN)

## Visão geral

- Tipo de operacao: `query`
- Objetivo: tem a responsabilide de acessar as informações do usuários

## Regras de acesso

| Operação | Tipo | Acesso | Permissões | Observações |
| --- | --- | --- | --- | --- |
| `list` | `query` | Protegido | `[ApiKeyPermission, SessionPermission]` | Regras resumidas de autorização |


## Operações

<!--Listar Registros-->
### `list`

#### Resumo

Objetivo do me é acessar informações dos usuários no sistema.

#### Assinatura do GraphQL

```graphql
query ListUsersSchema($input: ListInput!){
    admin {
        users {
            list (input: $input){
                root {
                    userId
                    name 
                    email
                    role,
                    password,
                    isDeleted,
                    createdAt,
                    updatedAt
                }    
            }
        }
        
    }
}
```

#### Variáveis

```json
{
    "input": {
        "pagination": {
            "all_": false,
            "page": 1,
            "limit": 1
        },
        "filterBy": {
            "role": "Status",
            "createdAt": "DD-MM-YYYY",
            "isDeleted": true
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

#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `all_` | `Boolean` | Sim | parâmetro direto | Buscar todos os registros | `true` |
| `page` | `Int` | Não | parâmetro direto | Divisão por página os registro |`1` |
| `limit` | `Int` | Não | parâmetro direto | Número de registros por página | `4` |
| `role` | `Roles` | Não | parâmetro direto | Papel de cada usuário | `ADMIN` |
| `createdAt` | `Datetime` | Não | parâmetro direto | Data do registros criados | `23-01-2026` |
| `isDeleted` | `Boolean` | Não | parâmetro direto | Número de registros por página | `false` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "admin": {
            "users": {
                "list": {
                    "root": [
                        {
                            "userId": "2caafd25-a9d9-4a63-8ffb-27db1febc506",
                            "name": "Kiss Martin",
                            "email": "kiss2@gmail.com",
                            "role": "USER",
                            "password": null,
                            "isDeleted": false,
                            "createdAt": 1776945291.11555,
                            "updatedAt": 1776945291.115559
                        }
                    ]
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

#### Estrutura de `error`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `message` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |


#### Exceções mapeadas

- `SessionError`: Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.
- `UnknownError`: Erro não identificado – fallback genérico.

<!--Selecionar ID específico-->
### `getById`

#### Resumo

Objetivo do me é acessar informações do usuário por seu respectivo ID no sistema.

#### Assinatura do GraphQL

```graphql
query GetByIdUser($userId: String!){
    admin {
        users {
            getById(userId: $userId){
                userId
                name 
                email 
                role
                password
                isDeleted
                createdAt 
                updatedAt 
            }       
        }
    }
}
```

#### Variáveis

```json
{
    "userId": "2caafd25-a9d9-4a63-8ffb-27db1febc506"
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
| `userId` | `String` | Sim | parâmetro direto | Buscar o registro por seu ID | `2caafd25-a9d9-4a63-8ffb-27db1febc506` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "admin": {
            "users": {
                "getById": {
                    "name": "Nome do Usuário",
                    "email": "usuario@exemplo.com",
                    "isDeleted": false,
                    "createdAt": 1776945291.11555,
                    "updatedAt": 1776945291.115559  
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



