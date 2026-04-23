# Auth Mutation

Documentação representa para autenticação do usuário

## Visão geral

- Tipo de operacao: `mutation`
- Objetivo: tem a responsabilidade de autenticar o usuário

## Regras de acesso

| Operação | Tipo | Acesso | Permissões | Observações |
| --- | --- | --- | --- | --- |
| `login` | `mutation` | Público | `[]` | Regras resumidas de autenticação/autorizacção |
| `verifyTwoFactor` | `mutation` | Público | `[]` | Regras resumidas de autenticação |
| `register` | `mutation` | Público | `[]` | Regras resumidas de autorização |
| `forgotPassword` | `mutation` | Público | `[]` | Regras resumidas de autenticação |
| `resetPassword` | `mutation` | Público | `[]` | Regras resumidas de autorização |

## Operações

<!--Autenticação-->
### `login`

#### Resumo

Objetivo da login é autenticar o usuário no sistema, para que tenha acesso as funcionalidades
baseado em seu papel.

#### Assinatura do GraphQL

```graphql
mutation AuthLogin($schema: UserLoginInput!){
    auth {
        login (schema: $schema) {
            success 
            data { token number expiresAt }
            error { errorName typeError statusCode }
            timestamp
        }
    }
}
```
#### Variáveis

```json
{ 
    "schema": {
        "email": "email@exemplo.com",
        "password": "senha"
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório |
| --- | --- | 
| `X-Api-Key` | Não 
| `Authorization` | Não | 


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `email` | `String` | Sim | parâmetro direto | E-mail registrado | `"email@exemplo.com"` |
| `password` | `String` | Sim | parâmetro direto | Senha registrada | `senha123` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "auth": {
            "login": {
                "success": true,
                "data": {
                    "token": "token",
                    "number": 0,
                    "expiresAt": 0
                },
                "error": null,
                "timestamp": 0
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
            "login": {
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

- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `InvalidCredentialsException`: Credenciais de autenticação inválidas.
- `UnknownError`: Erro não identificado – fallback genérico.

<!--Registar usuário-->
### `register`

#### Resumo

Objetivo da register é registrar novo usuário no sistema.

#### Assinatura do GraphQL

```graphql
mutation UserCreateSchema ($schema: UserInput!) {
    auth {
        register(schema: $schema) {
            success
            data {  name email createdAt updatedAt}
            error { errorName typeError statusCode }
        }
    }

}
```
#### Variáveis

```json
{    
    "schema": {
        "name": "Nome Usuário",
        "email": "usuario@exemplo.com",
        "password": "usuariosenha"
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório |
| --- | --- | 
| `X-Api-Key` | Não 
| `Authorization` | Não | 


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatório | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `name` | `String` | Sim | parâmetro direto | Nome do usuário | `"Nome Usuário"` |
| `email` | `String` | Sim | parâmetro direto | E-mail do usuário | `"usuario@exemplo.com"` |
| `password` | `String` | Sim | parâmetro direto | Senha do usuário | `"usuariosenha"` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "auth": {
            "register": {
                "success": true,
                "data": {
                    "name": "Nome Usuário",
                    "email": "email@exemplo.com",
                    "createdAt": 1775228778.306308,
                    "updatedAt": 1776944662.517973
                },
                "error": null
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
            "register": {
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

- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `EntityValidationError`: Falha de validação ao inserir ou atualizar dados de uma entidade.
- `DuplicateReviewError`: Tentativa de inserir um registro duplicado.
- `UnknownError`: Erro não identificado – fallback genérico.


<!--Verificação de dois fatores-->
### `verifyTwoFactor`

#### Resumo

Objetivo da verifyTwoFactor é autenticar o usuário no sistema, para que tenha acesso as funcionalidades por meio de uma sessão.

#### Assinatura do GraphQL

```graphql
mutation Verify2FASchema($schema: Verify2FAInput!){
    auth {
        verifyTwoFactor (schema: $schema) {
            success 
            data { sessionId createdAt expiresAt }
            error { errorName typeError statusCode }
        }
    }

}
```
#### Variáveis

```json
{ 
    "schema": {
        "token": "eyJhbGciOiJIUzI1N...",
        "number": 850849
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório |
| --- | --- | 
| `X-Api-Key` | Não 
| `Authorization` | Não | 


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `token` | `String` | Sim | parâmetro direto | Token fornecido no login | `"eyJhbGciOiJIUz...."` |
| `password` | `Int` | Sim | parâmetro direto | Número enviado para e-mail | 850849 |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json

{
    "data": {
        "auth": {
            "verifyTwoFactor": {
                "success": true,
                "data": {
                    "sessionId": "eyJhbGciOiJIUzI1NiI...",
                    "createdAt": 1776943527.151267,
                    "expiresAt": 1776954327.151267
                },
                "error": null
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
            "verifyTwoFactor": {
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

- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `InvalidCredentialsException`: Credenciais de autenticação inválidas.
- `ExpirationError`: Recurso ou sessão expirada.
- `UnknownError`: Erro não identificado – fallback genérico.


<!--Verificação de e-mail para resete-->
### `forgotPassword`

#### Resumo

Objetivo da forgotPassword é verificar a existência do usuário no sistema, para que tenha possa enviar e-mail de notificação para e-mail.

#### Assinatura do GraphQL

```graphql
mutation ForgotPasswordSchema($schema: ForgotPasswordInput!) {
    auth {
        forgotPassword(schema: $schema) {
            success
            data {
                token
                expiresAt
            }
            error { errorName typeError statusCode }
        }
    }
}
```
#### Variáveis

```json
{
    "schema": {
        "email": "email@exemplo.com"
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório |
| --- | --- | 
| `X-Api-Key` | Não 
| `Authorization` | Não | 


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `email` | `String` | Sim | parâmetro direto | E-mail registrado | `"email@exemplo.com"` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "auth": {
            "forgotPassword": {
                "success": true,
                "data": {
                    "token": "eyJhbGciOiJIUzI1NiI...",
                    "expiresAt": 1776944908.912749
                },
                "error": null
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
            "forgotPassword": {
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

- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `InvalidCredentialsException`: Credenciais de autenticação inválidas.
- `UnknownError`: Erro não identificado – fallback genérico.

<!--Nova senha-->
### `resetPassword`

#### Resumo

Objetivo da resetPassword é renovar a senha do usuário no sistema.

#### Assinatura do GraphQL

```graphql
mutation ResetPasswordSchema($schema: UserResetPasswordInput!) {
    auth {
        resetPassword(schema: $schema) {
            success
            data {
                name
                email
                createdAt
                updatedAt  
            }
            error { errorName typeError statusCode }
        }
    }
        
}
```
#### Variáveis

```json
{
    "schema": {
        "token": "eyJhbGciOiJIUzI...",
        "password": "novasenha"
    }
}
```

#### Headers

- Contexto necessario:

| Header | Obrigatório |
| --- | --- | 
| `X-Api-Key` | Não 
| `Authorization` | Não | 


#### Argumentos

| Argumento | Tipo GraphQL | Obrigatorio | Origem no codigo | Descrição | Exemplo |
| --- | --- | --- | --- | --- | --- |
| `token` | `String` | Sim | parâmetro direto | Token fornecido pela verificação de e-mail | `"eyJhbGciOiJIUz...."` |
| `password` | `String` | Sim | parâmetro direto | Nova senha | `"novasenha"` |

#### Estrutura ideal da resposta

Todas as operações deste projeto retornam um `ApiResponseType[Sucesso, ApiErrorType]`.

##### Sucesso

```json
{
    "data": {
        "auth": {
            "resetPassword": {
                "success": true,
                "data": {
                    "name": "Nome Usuário",
                    "email": "email@exemplo.com",
                    "createdAt": 1775228778.306308,
                    "updatedAt": 1776944662.517973
                },
                "error": null
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
            "resetPassword": {
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

- `InvalidFieldsException`: Campos obrigatórios estão ausentes ou inválidos.
- `InvalidCredentialsException`: Credenciais de autenticação inválidas.
- `UnprocessableEntity`: Erro de consistência ou semântica nos dados.
- `UnknownError`: Erro não identificado – fallback genérico.















