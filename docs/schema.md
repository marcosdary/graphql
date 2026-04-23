# Schema GraphQL

Documentacao de referencia do arquivo `schema.graphql`.

## Visao geral

- Arquivo: `schema.graphql`
- Objetivo: definir o contrato GraphQL exposto pela aplicacao, incluindo scalars, enums, types, inputs, unions, queries e mutations.
- Estilo da API: respostas padronizadas via `ApiResponseType`, com payload dinamico em `data` e estrutura de erro em `ApiErrorType`.

## Estrutura do schema

O schema esta organizado em:

- `scalar`: tipos customizados para datas.
- `enum`: valores fechados usados em inputs e retornos.
- `type`: objetos de resposta e agrupadores de operacoes.
- `input`: objetos de entrada para queries e mutations.
- `union`: composicao dos tipos possiveis retornados em `ApiResponseType.data`.
- `Query`: ponto de entrada para leitura de dados.
- `Mutation`: ponto de entrada para escrita e alteracao de dados.

## Scalars customizados

| Scalar | Descricao | Exemplo |
| --- | --- | --- |
| `DateTime` | Data e hora em formato ISO 8601 | `"2026-04-16T14:30:00Z"` |
| `Date` | Data sem horario | `"2026-04-16"` |

## Enums

### `Roles`

| Valor | Descricao |
| --- | --- |
| `USER` | Usuario comum |
| `ADMIN` | Usuario com privilegios administrativos |
| `SUPER_ADMIN` | Papel maximo do sistema |

### `ExpirationApiKey`

| Valor | Descricao |
| --- | --- |
| `ONE_HOUR` | Expiracao de 1 hora |
| `ONE_DAY` | Expiracao de 1 dia |
| `TWO_DAYS` | Expiracao de 2 dias |
| `SEVEN_DAYS` | Expiracao de 7 dias |
| `THIRTY_DAYS` | Expiracao de 30 dias |
| `NINETY_DAYS` | Expiracao de 90 dias |
| `ONE_YEAR` | Expiracao de 1 ano |

## Tipos compartilhados

### `ApiErrorType`

Payload padrao de erro retornado nas operacoes.

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `errorName` | `String!` | Mensagem legivel do erro |
| `typeError` | `String!` | Nome da classe da excecao |
| `statusCode` | `Int` | Codigo HTTP/logico associado ao erro |

### `ApiResponseType`

Envelope padrao das respostas de sucesso e erro.

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `success` | `Boolean!` | Indica se a operacao foi concluida com sucesso |
| `data` | `Data` | Payload principal; usa a union `Data` |
| `error` | `ApiErrorType` | Dados do erro quando `success=false` |
| `timestamp` | `Float!` | Momento em que a resposta foi montada |

Observacao:

- O schema publicado usa `timestamp: Float!`, mas a implementacao Python monta esse valor a partir de `datetime.now()` em `build_response`.

## Types de dominio

### `UserPublicType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `name` | `String` | Nome do usuario |
| `email` | `String!` | E-mail do usuario |
| `createdAt` | `DateTime` | Data de criacao |
| `updatedAt` | `DateTime` | Data da ultima atualizacao |

### `UserPrivateType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `userId` | `String!` | Identificador unico do usuario |
| `name` | `String` | Nome do usuario |
| `email` | `String!` | E-mail do usuario |
| `password` | `String` | Senha persistida ou hash conforme serializacao |
| `role` | `Roles` | Papel do usuario |
| `isDeleted` | `Boolean` | Indicador de exclusao |
| `createdAt` | `DateTime` | Data de criacao |
| `updatedAt` | `DateTime` | Data da ultima atualizacao |

### `SessionType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `sessionId` | `String!` | Identificador da sessao |
| `createdAt` | `DateTime!` | Data de criacao da sessao |
| `expiresAt` | `DateTime!` | Data de expiracao da sessao |

### `TwoFactorAuthType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `token` | `String!` | Token temporario do fluxo 2FA |
| `number` | `Int!` | Codigo numerico do segundo fator |
| `expiresAt` | `DateTime` | Data de expiracao do desafio 2FA |

### `ApiKeyType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `token` | `String` | Token da API Key |
| `expiresAt` | `DateTime` | Expiracao da API Key |

### `UserListType`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `items` | `[UserPrivateType]` | Lista de usuarios retornados |
| `total` | `Int` | Total de registros |
| `page` | `Int` | Pagina atual |
| `limit` | `Int` | Limite por pagina |
| `hasNextPage` | `Boolean` | Indica se existem mais paginas |

## Inputs

### `UserInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `name` | `String` | Nao | Nome do usuario |
| `email` | `String` | Nao | E-mail do usuario |
| `password` | `String` | Nao | Senha do usuario |

### `UserPrivateInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `name` | `String` | Nao no SDL | Nome do usuario |
| `email` | `String` | Nao no SDL | E-mail do usuario |
| `password` | `String` | Nao no SDL | Senha inicial |
| `role` | `Roles` | Nao no SDL | Papel do usuario |

### `UserUpdatePublicInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `name` | `String` | Nao | Novo nome do usuario autenticado |

### `UserUpdatePrivateInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `userId` | `String!` | Sim | Identificador do usuario a atualizar |
| `name` | `String` | Nao | Novo nome |
| `email` | `String` | Nao | Novo e-mail |
| `role` | `Roles` | Nao | Novo papel |
| `password` | `String` | Nao | Nova senha |

### `UserLoginInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `email` | `String!` | Sim | E-mail de login |
| `password` | `String!` | Sim | Senha de login |

### `PaginationInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `page` | `Int` | Nao | Numero da pagina |
| `limit` | `Int` | Nao | Tamanho da pagina |
| `all_` | `Boolean` | Nao | Quando `true`, desativa a paginacao por pagina/limite |

### `FilterByInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `name` | `String` | Nao | Filtra por nome |
| `createdAt` | `Date` | Nao | Filtra por data de criacao |
| `isDeleted` | `Boolean` | Nao | Filtra por estado de exclusao |
| `role` | `Roles` | Nao | Filtra por papel |

### `Verify2FAInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `number` | `Int!` | Sim | Codigo numerico do 2FA |
| `token` | `String!` | Sim | Token do desafio 2FA |

### `ForgotPasswordInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `email` | `String!` | Sim | E-mail para recuperacao de senha |

### `UserResetPasswordInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `password` | `String!` | Sim | Nova senha |
| `token` | `String!` | Sim | Token de redefinicao |

### `ApiKeyInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `expiration` | `ExpirationApiKey` | Nao | Periodo de expiracao da chave |

### `ListInput`

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| `pagination` | `PaginationInput!` | Sim | Configuracao de paginacao |
| `filterBy` | `FilterByInput` | Nao | Filtros de busca |

## Union `Data`

`ApiResponseType.data` pode retornar um dos seguintes tipos:

- `UserPublicType`
- `UserPrivateType`
- `ApiKeyType`
- `SessionType`
- `TwoFactorAuthType`
- `UserListType`
- `Boolean`

Observacao:

- Algumas operacoes tipadas em Python retornam `None` em sucesso mesmo quando a intencao semantica do SDL sugere `Boolean`, como em exclusoes com `build_response(True)` sem payload explicito.

## Ponto de entrada de queries

### `Query`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `account` | `AccountQuery` | Agrupa consultas do usuario autenticado |
| `admin` | `AdminQuery` | Agrupa consultas administrativas |

### `AccountQuery`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `me` | `ApiResponseType!` | Retorna os dados do usuario autenticado |

### `AdminQuery`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `users` | `AdminUserQuery` | Agrupa consultas administrativas de usuarios |

### `AdminUserQuery`

| Campo | Assinatura | Descricao |
| --- | --- | --- |
| `list` | `list(input: ListInput): ApiResponseType!` | Lista usuarios com paginacao e filtros |
| `getById` | `getById(userId: String!): ApiResponseType!` | Busca um usuario por identificador |

## Ponto de entrada de mutations

### `Mutation`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `admin` | `AdminMutation` | Agrupa operacoes administrativas |
| `user` | `AccountMutation` | Agrupa operacoes de conta do usuario autenticado |
| `auth` | `AuthMutation` | Agrupa autenticacao, cadastro e recuperacao |

### `AdminMutation`

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `users` | `AdminUserMutation` | Operacoes administrativas de usuarios |
| `apiKey` | `AdminApiKeyMutation` | Operacoes administrativas de API Keys |

### `AdminUserMutation`

| Campo | Assinatura | Descricao |
| --- | --- | --- |
| `create` | `create(schema: UserPrivateInput!): ApiResponseType!` | Cria usuario em contexto administrativo |
| `update` | `update(schema: UserUpdatePrivateInput!): ApiResponseType!` | Atualiza usuario em contexto administrativo |
| `delete` | `delete(userId: String!): ApiResponseType!` | Remove usuario por ID |

### `AdminApiKeyMutation`

| Campo | Assinatura | Descricao |
| --- | --- | --- |
| `create` | `create(schema: ApiKeyInput!): ApiResponseType!` | Gera nova API Key |
| `delete` | `delete(key: String!): ApiResponseType!` | Remove API Key existente |

### `AccountMutation`

| Campo | Assinatura | Descricao |
| --- | --- | --- |
| `updateProfile` | `updateProfile(schema: UserUpdatePublicInput): ApiResponseType!` | Atualiza o proprio perfil |
| `deleteAccount` | `deleteAccount: ApiResponseType!` | Remove a propria conta |

### `AuthMutation`

| Campo | Assinatura | Descricao |
| --- | --- | --- |
| `register` | `register(schema: UserInput): ApiErrorType!` | Cadastra usuario |
| `login` | `login(schema: UserLoginInput!): ApiResponseType!` | Inicia autenticacao |
| `verifyTwoFactor` | `verifyTwoFactor(schema: Verify2FAInput): ApiResponseType!` | Conclui autenticacao com 2FA |
| `forgotPassword` | `forgotPassword(schema: ForgotPasswordInput): ApiResponseType!` | Solicita recuperacao de senha |
| `resetPassword` | `resetPassword(schema: UserResetPasswordInput): ApiResponseType!` | Redefine a senha a partir de token |

## Fluxo de navegacao da API

Exemplos de caminhos validos no schema:

- Query de conta: `account.me`
- Query administrativa: `admin.users.list`
- Mutation administrativa de usuarios: `admin.users.create`
- Mutation administrativa de API Key: `admin.apiKey.create`
- Mutation de autenticacao: `auth.login`
- Mutation de conta autenticada: `user.updateProfile`

## Observacoes de compatibilidade

- O schema centraliza o contrato publicado, mas alguns detalhes de obrigatoriedade podem diferir da validacao real feita pelos DTOs e repositorios.
- A union `Data` existe para acomodar multiplos payloads em um envelope unico de resposta.
- Para detalhes de cada operacao, consulte as documentacoes especificas em `docs/queries` e `docs/mutations`.
