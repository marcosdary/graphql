# AdminUserMutation

Documentacao das operacoes definidas em `app/graphql/mutations/admin_user_mutation.py`.

## Visao geral

- Tipo de operacao: `mutation`
- Objetivo: expor operacoes administrativas para criar, atualizar e remover usuarios via GraphQL.

## Regras de acesso

| Operacao | Tipo | Acesso | Permissoes | Observacoes |
| --- | --- | --- | --- | --- |
| `create` | `mutation` | Protegido | `[ApiKeyPermission, SessionPermission, RolePermission]` | Exige API Key, sessao valida e usuario com role diferente de `USER` |
| `update` | `mutation` | Protegido | `[ApiKeyPermission, SessionPermission, RolePermission]` | Exige API Key, sessao valida e usuario com role diferente de `USER` |
| `delete` | `mutation` | Protegido | `[ApiKeyPermission, SessionPermission, RolePermission]` | Exige API Key, sessao valida e usuario com role diferente de `USER` |

## Operações

### `create`

#### Resumo

Cria um novo usuario em contexto administrativo a partir de um `UserPrivateInput`.

#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descricao | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `schema` | `UserPrivateInput` | Sim | input object | Dados do usuario a ser criado | `{ "name": "Maria", "email": "maria@acme.com", "password": "123456", "role": "ADMIN" }` |


#### Assinatura do GraphQL

```graphql
mutation AdminUserCreate($schema: UserPrivateInput!) {
  admin {
    users {
      create(schema: $schema) {
        success
        data {
          userId
          name
          email
          password
          role
          isDeleted
          createdAt
          updatedAt
        }
        error {
          typeError
          errorName
          statusCode
        }
        timestamp
      }
    }
  }
}
```

#### Variáveis

```json
{
  "schema": {
    "name": "Maria Silva",
    "email": "maria@acme.com",
    "password": "123456",
    "role": "ADMIN"
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

##### `UserPrivateInput`

| Campo | Tipo GraphQL | Obrigatorio | Descricao | Exemplo |
| --- | --- | --- | --- | --- |
| `name` | `String` | Sim | Nome do usuario | `"Maria Silva"` |
| `email` | `String` | Sim | E-mail do usuario; o DTO valida o formato | `"maria@acme.com"` |
| `password` | `String` | Sim | Senha inicial do usuario | `"123456"` |
| `role` | `Roles` | Sim | Papel do usuario a ser criado | `"ADMIN"` |

#### Estrutura ideal da resposta

Todas as operacoes deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
  "data": {
    "admin": {
      "users": {
        "create": {
          "success": true,
          "data": {
            "userId": "usr_123",
            "name": "Maria Silva",
            "email": "maria@acme.com",
            "password": "$2b$12$hash...",
            "role": "ADMIN",
            "isDeleted": false,
            "createdAt": "2026-04-23T12:00:00-03:00",
            "updatedAt": "2026-04-23T12:00:00-03:00"
          },
          "error": null,
          "timestamp": "2026-04-23T12:00:00"
        }
      }
    }
  }
}
```

##### Erro

```json
{
  "data": {
    "admin": {
      "users": {
        "create": {
          "success": false,
          "data": null,
          "error": {
            "typeError": "DuplicateReviewError",
            "errorName": "Email esta em uso.",
            "statusCode": 409
          },
          "timestamp": "2026-04-23T12:00:00"
        }
      }
    }
  }
}
```

#### Estrutura do retorno

| Campo | Tipo | Sempre presente | Descricao |
| --- | --- | --- | --- |
| `success` | `bool` | Sim | Indica se a operacao foi concluida com sucesso |
| `data` | `UserPrivateType \| null` | Sim | Payload de sucesso da operacao |
| `error` | `ApiErrorType \| null` | Sim | Payload de erro quando `success=false` |
| `timestamp` | `datetime` | Sim | Data e hora em que `build_response` montou a resposta |

#### Estrutura de `error`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `errorName` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |

#### Headers relevantes

| Header | Quando aparece | Significado |
| --- | --- | --- |
| `Last-Modified` | Em caso de sucesso | Data de criacao do usuario retornado, escrita a partir de `data.createdAt` |

#### Tipos retornados em `data`

##### `UserPrivateType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `userId` | `String` | Identificador unico do usuario |
| `name` | `String \| null` | Nome do usuario |
| `email` | `String` | E-mail do usuario |
| `password` | `String \| null` | Senha persistida em formato hash |
| `role` | `String \| null` | Papel do usuario no sistema |
| `isDeleted` | `Boolean \| null` | Indicador de exclusao logica no modelo de leitura |
| `createdAt` | `String \| null` | Data de criacao serializada em ISO 8601 com timezone `America/Sao_Paulo` |
| `updatedAt` | `String \| null` | Data de atualizacao serializada em ISO 8601 com timezone `America/Sao_Paulo` |

#### Regras de negocio

- O input GraphQL e convertido com `schema.to_pydantic()` antes de chegar ao repositorio.
- O e-mail nao pode estar em uso; duplicidade gera `DuplicateReviewError`.
- O repositorio impede a criacao de usuario com role `SUPER_ADMIN`.
- A senha informada e transformada em hash antes da persistencia.

#### Excecoes mapeadas

- `DuplicateReviewError`: Tentativa de inserir um registro duplicado.
- `EntityValidationError`: Falha de validação ao inserir ou atualizar dados de uma entidade.
- `ExpirationError`: Recurso ou sessão expirada.
- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `SessionError`: Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.
- `UnprocessableEntity`: Erro de consistência ou semântica nos dados.
- `UnknownError`: Erro não identificado – fallback genérico.

#### Observacoes de implementacao

- Escreve `Last-Modified` no `info.context["response"]`.
- Depende das permissoes para validar API Key, sessao e role administrativa.

### `update`

#### Resumo

Atualiza dados de um usuario existente por meio de um `UserUpdatePrivateInput`.

#### Assinatura no codigo


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descricao | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `schema` | `UserUpdatePrivateInput` | Sim | input object | Dados parciais da atualizacao; `userId` identifica o usuario alvo | `{ "userId": "usr_123", "name": "Maria Souza", "role": "ADMIN" }` |

#### Input object detalhado

##### `UserUpdatePrivateInput`

| Campo | Tipo GraphQL | Obrigatorio | Descricao | Exemplo |
| --- | --- | --- | --- | --- |
| `userId` | `String` | Nao | Identificador do usuario a ser alterado | `"usr_123"` |
| `name` | `String` | Nao | Novo nome do usuario | `"Maria Souza"` |
| `email` | `String` | Nao | Novo e-mail do usuario | `"maria.souza@acme.com"` |
| `role` | `Roles` | Nao | Novo papel do usuario | `"ADMIN"` |
| `password` | `String` | Nao | Nova senha; sera convertida para hash pelo serializer do DTO | `"654321"` |

#### Assinatura do GraphQL

```graphql
mutation AdminUserUpdate($schema: UserUpdatePrivateInput!) {
  admin {
    users {
      update(schema: $schema) {
        success
        data {
          userId
          name
          email
          password
          role
          isDeleted
          createdAt
          updatedAt
        }
        error {
          typeError
          errorName
          statusCode
        }
        timestamp
      }
    }
  }
}
```

#### Variáveis

```json
{
  "schema": {
    "userId": "usr_123",
    "name": "Maria Souza",
    "email": "maria.souza@acme.com",
    "role": "ADMIN"
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

Todas as operacoes deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
  "data": {
    "admin": {
      "users": {
        "update": {
          "success": true,
          "data": {
            "userId": "usr_123",
            "name": "Maria Souza",
            "email": "maria.souza@acme.com",
            "password": "$2b$12$hash...",
            "role": "ADMIN",
            "isDeleted": false,
            "createdAt": "2026-04-23T12:00:00-03:00",
            "updatedAt": "2026-04-23T12:10:00-03:00"
          },
          "error": null,
          "timestamp": "2026-04-23T12:10:00"
        }
      }
    }
  }
}
```

##### Erro

```json
{
  "data": {
    "admin": {
      "users": {
        "update": {
          "success": false,
          "data": null,
          "error": {
            "typeError": "NotFoundError",
            "errorName": "Usuario nao encontrado ou removido do sistema.",
            "statusCode": 404
          },
          "timestamp": "2026-04-23T12:10:00"
        }
      }
    }
  }
}
```

#### Estrutura do retorno

| Campo | Tipo | Sempre presente | Descricao |
| --- | --- | --- | --- |
| `success` | `bool` | Sim | Indica se a operacao foi concluida com sucesso |
| `data` | `UserPrivateType \| null` | Sim | Payload de sucesso da operacao |
| `error` | `ApiErrorType \| null` | Sim | Payload de erro quando `success=false` |
| `timestamp` | `datetime` | Sim | Data e hora em que `build_response` montou a resposta |

#### Estrutura de `error`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `errorName` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |

#### Headers relevantes

| Header | Quando aparece | Significado |
| --- | --- | --- |
| `Last-Modified` | Em caso de sucesso | O codigo escreve o header com base em `data.createdAt` |

#### Tipos retornados em `data`

##### `UserPrivateType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `userId` | `String` | Identificador unico do usuario |
| `name` | `String \| null` | Nome do usuario |
| `email` | `String` | E-mail do usuario |
| `password` | `String \| null` | Senha persistida em formato hash |
| `role` | `String \| null` | Papel do usuario no sistema |
| `isDeleted` | `Boolean \| null` | Indicador de exclusao logica no modelo de leitura |
| `createdAt` | `String \| null` | Data de criacao serializada em ISO 8601 com timezone `America/Sao_Paulo` |
| `updatedAt` | `String \| null` | Data de atualizacao serializada em ISO 8601 com timezone `America/Sao_Paulo` |

#### Regras de negócio

- O input GraphQL e convertido com `schema.to_pydantic()`.
- O usuario alvo precisa existir e nao estar removido; caso contrario, retorna `NotFoundError`.
- Somente os campos nao nulos enviados no schema sao aplicados no modelo.
- A atualizacao para role `SUPER_ADMIN` e rejeitada pelo repositorio.
- Se `password` for enviada, o DTO serializa o valor para hash antes da persistencia.

#### Exceções mapeadas

- `NotFoundError`: Erro quando um recurso solicitado não é encontrado.
- `DuplicateReviewError`: Tentativa de inserir um registro duplicado.
- `EntityValidationError`: Falha de validação ao inserir ou atualizar dados de uma entidade.
- `ExpirationError`: Recurso ou sessão expirada.
- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `SessionError`: Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.
- `UnprocessableEntity`: Erro de consistência ou semântica nos dados.
- `UnknownError`: Erro não identificado – fallback genérico.


### `delete`

#### Resumo

Remove um usuario a partir do `userId` informado.

#### Acesso

- Tipo: `mutation`
- Protegida por permissao: `sim`
- `permission_classes`: `[ApiKeyPermission, SessionPermission, RolePermission]`
- Contexto necessario:
- `api_key`: sim
- `Authorization: Bearer <session_id>`: sim
- Role especifica: sim, a permissao bloqueia usuarios com role `USER`

#### Assinatura do GraphQL

```graphql
mutation AdminUserDelete($userId: String!) {
  admin {
    users {
      delete(userId: $userId) {
        success
        data
        error {
          typeError
          errorName
          statusCode
        }
        timestamp
      }
    }
  }
}
```

#### Variáveis

```json
{
  "userId": "usr_123"
}
```

#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descricao | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `userId` | `String` | Sim | parametro direto | Identificador do usuario a ser removido | `"usr_123"` |

#### Headers

- Contexto necessario:

| Header | Obrigatório | Tipo | Exemplo | 
| --- | --- | --- | --- | 
| `X-Api-Key` | Sim | String | `"eyJhbGciOiJIUz...."` |
| `Authorization` | Sim | Bearer token | `"Bearer eyJhbGciOiJIUz...."` |

#### Estrutura ideal da resposta

Todas as operacoes deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
  "data": {
    "admin": {
      "users": {
        "delete": {
          "success": true,
          "data": null,
          "error": null,
          "timestamp": "2026-04-23T12:20:00"
        }
      }
    }
  }
}
```

##### Erro

```json
{
  "data": {
    "admin": {
      "users": {
        "delete": {
          "success": false,
          "data": null,
          "error": {
            "typeError": "ForbiddenActionError",
            "errorName": "Acao nao permitida. Nao pode apagar o ADMIN. Por favor, entre em contato com o suporte",
            "statusCode": 403
          },
          "timestamp": "2026-04-23T12:20:00"
        }
      }
    }
  }
}
```

#### Estrutura do retorno

| Campo | Tipo | Sempre presente | Descricao |
| --- | --- | --- | --- |
| `success` | `bool` | Sim | Indica se a operacao foi concluida com sucesso |
| `data` | `bool \| null` | Sim | O metodo tipa `bool`, mas `build_response(True)` retorna sem payload explicito em caso de sucesso |
| `error` | `ApiErrorType \| null` | Sim | Payload de erro quando `success=false` |
| `timestamp` | `datetime` | Sim | Data e hora em que `build_response` montou a resposta |

#### Estrutura de `error`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `typeError` | `string` | Nome da classe da excecao |
| `errorName` | `string` | Mensagem retornada pela excecao |
| `statusCode` | `int` | Codigo HTTP/logico associado ao erro |

#### Regras de negocio

- O usuario precisa existir; caso contrario, retorna `NotFoundError`.
- O repositorio impede a exclusao de usuario com role `SUPER_ADMIN`.
- A operacao remove o registro via `session.delete(user)`.

#### Excecoes mapeadas

- `NotFoundError`: Erro quando um recurso solicitado não é encontrado.
- `ExpirationError`: Recurso ou sessão expirada.
- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `SessionError`: Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.
- `UnprocessableEntity`: Erro de consistência ou semântica nos dados.
- `UnknownError`: Erro não identificado – fallback genérico.

#### Observacoes de implementacao

- Usa `build_response` para padronizar a resposta.
- Nao escreve headers extras no `response`.
