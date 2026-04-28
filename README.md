# Graph API

Graph API é um backend FastAPI + Strawberry GraphQL focado em autenticação, gerenciamento de usuários, manipulação de sessões, proteção por chaves de API e um endpoint de webhook para validação de payloads assinados.

O projeto utiliza PostgreSQL para persistência, Redis para armazenamento temporário de tokens e sessões, e tokens JWT assinados para chaves de API, sessões, 2FA e fluxos de redefinição de senha.

## Visão Geral

Este serviço expõe:

- Um endpoint `GET /` do tipo health check com metadados básicos da aplicação
- Um endpoint `POST /webhook` protegido por `x-webhook-secret`
- Uma API GraphQL em `/graphql`

A camada GraphQL suporta:

- Registro de usuários
- Login com autenticação de dois fatores (2FA)
- Criação e validação de sessões
- Fluxo de redefinição de senha
- Acesso e atualização de perfil do usuário autenticado
- Exclusão lógica (soft delete) de usuários
- Operações protegidas para admin e super-admin
- Geração e revogação de chaves de API

## Stack Tecnológica

- Python 3.12+
- FastAPI
- Strawberry GraphQL
- SQLAlchemy
- PostgreSQL
- Redis
- PyJWT
- Pydantic / pydantic-settings
- Uvicorn
- Gunicorn

## Arquitetura

O código está organizado em uma estrutura em camadas bastante padrão:

- `app/main.py`: Inicialização da aplicação FastAPI, configuração de CORS, roteador de webhook e roteador GraphQL
- `app/config/`: Configurações de ambiente, engines do banco de dados e clientes Redis
- `app/constants/`: Constantes do ambiente, representados por enum.
- `app/models/`: Modelos SQLAlchemy
- `app/dto/`: Modelos Pydantic usados entre as camadas
- `app/repositories/`: Lógica de acesso e persistência no banco de dados
- `app/services/`: Serviços de tokens, hash de senhas, helpers de cache, rate limiting e integrações externas
- `app/graphql/`: Composição do schema, queries, mutations, inputs, types, permissões e helpers de resposta
- `app/routes/`: Rotas HTTP não-GraphQL
- `app/clients/`: Integrações com clientes externos
- `app/utils/`: Pequenos utilitários auxiliares
- `tests/`: Testes unitários e testes assíncronos de permissões

## Principais Áreas Funcionais

### Autenticação

O fluxo de autenticação é dividido em múltiplas etapas:

1. `login` valida o e-mail e a senha.
2. Um token temporário de dois fatores e um código numérico são gerados e armazenados no Redis.
3. `verifyTwoFactor` consome o token temporário de 2FA e cria um token de sessão.
4. Operações protegidas utilizam o token de sessão através do header `session-id`.

### Proteção por Chave de API

Algumas operações GraphQL também exigem uma chave de API no header `Authorization`:

- Formato: `Authorization: Bearer <api-key>`

As chaves de API são assinadas e armazenadas no Redis com tempo de expiração. Os resolvers protegidos validam o token antes de executar a operação.

### Autorização Baseada em Roles

O projeto define três roles:

- `USER`
- `ADMIN`
- `SUPER_ADMIN`

Rotas exclusivas de admin são aplicadas através de classes de permissão do Strawberry. O acesso é validado a partir do payload da sessão atual e verificado contra uma lista de resolvers permitidos.

### Redefinição de Senha

O fluxo de redefinição de senha também utiliza tokens com expiração armazenados no Redis:

1. `forgotPassword` gera um token de redefinição.
2. `resetPassword` valida e consome esse token.
3. A senha do usuário é atualizada após a verificação do token.

### Validação de Webhook

A rota `/webhook`:

- Exige o header `x-webhook-secret` compatível com `WEBHOOK_SECRET`
- Espera um payload JSON com o campo `data`
- Decodifica o token assinado usando HS256
- Retorna `204 No Content` quando o payload é aceito

## Camada de Dados

O modelo atual do banco de dados inclui a tabela `users` com:

- `userId`
- `name`
- `role`
- `email`
- `isDeleted`
- `password`
- `createdAt`
- `updatedAt`

Existe um helper no repositório para remover fisicamente usuários inativos, mas ele não está exposto pela API pública no momento.

## Uso do Redis

O Redis é utilizado como armazenamento de curta duração para:

- Sessões
- Chaves de API
- Códigos de autenticação de dois fatores
- Tokens de redefinição de senha
- Contadores de rate limit

Tempos de expiração atualmente definidos no código:

- Sessão: 3 horas
- Autenticação de dois fatores: 10 minutos
- Redefinição de senha: 15 minutos

## Resumo do Schema GraphQL

### Queries

- `account.me`
- `admin.users.list`
- `admin.users.getById`

### Mutations

- `auth.register`
- `auth.login`
- `auth.verifyTwoFactor`
- `account.update`
- `account.delete`
- `auth.forgotPassword`
- `auth.resetPassword`
- `admin.apikey.create`
- `admin.users.create`
- `admin.users.update`
- `admin.users.delete`
- `admin.apikey.delete`

### Principais Tipos GraphQL

- `UserPublicType`
- `UserPrivateType`
- `SessionType`
- `TwoFactorAuthType`
- `ApiKeyType`
- `ApiResponseType`
- `ApiErrorType`

## Autenticação e Headers

Dependendo do resolver, a API pode exigir um ou ambos os headers abaixo:

- `Authorization: Bearer <session-token>`
- `api-key: <api-key>`

Proteção dos resolvers na prática:

- Públicos: `login`, `verifyTwoFactor`, `forgotPassword`, `resetPassword`
- Apenas chave de API: `auth.register`, `auth.login`, `auth.verifyTwoFactor`, `auth.resetPassword`
- Chave de API + sessão: `account.me`, `account.update`, `account.delete`
- Rotas com sessão protegidas por role: `admin.apikey.create`, `admin.users.create`, `admin.users.update`, `admin.users.delete`, `admin.apikey.delete`, `admin.users.list`, `admin.users.getById`

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e defina os seguintes valores:

| Variável                  | Propósito |
|---------------------------|---------|
| `REDIS_URL`               | String de conexão do Redis |
| `DATABASE_URL`            | String de conexão síncrona do PostgreSQL |
| `DATABASE_URL_ASYNC`      | String de conexão assíncrona do PostgreSQL |
| `CREATE_API_KEY`          | Segredo usado para assinar chaves de API |
| `PASSWORD_RESET_KEY`      | Segredo usado para assinar tokens de redefinição de senha |
| `TWO_FACTOR_AUTH_KEY`     | Segredo usado para assinar tokens de 2FA |
| `SESSION_KEY`             | Segredo usado para assinar sessões |
| `API_KEY`                 | Chave de API usada ao chamar o sistema de notificações externo |
| `URL_NOTIFICATION_SYSTEM` | Endpoint GraphQL do serviço de notificações |
| `WEBHOOK_SECRET`          | Segredo compartilhado usado pelo `/webhook` |

Exemplo:

```env
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/graph
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:postgres@localhost:5432/graph
CREATE_API_KEY=change-me
PASSWORD_RESET_KEY=change-me
TWO_FACTOR_AUTH_KEY=change-me
SESSION_KEY=change-me
API_KEY=change-me
URL_NOTIFICATION_SYSTEM=http://localhost:9000/graphql
WEBHOOK_SECRET=change-me
```