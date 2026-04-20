# Graph API

Graph API is a FastAPI + Strawberry GraphQL backend focused on authentication, user management, session handling, API key protection, and a webhook endpoint for signed payload validation.

The project uses PostgreSQL for persistence, Redis for temporary token/session storage, and JWT-based signed tokens for API keys, sessions, 2FA, and password reset flows.

## Overview

This service exposes:

- A `GET /` health-style endpoint with basic app metadata
- A `POST /webhook` endpoint protected by `x-webhook-secret`
- A GraphQL API at `/graphql`

The GraphQL layer supports:

- User registration
- Login with two-factor authentication
- Session creation and validation
- Password reset flow
- Authenticated user profile access and update
- Soft deletion of users
- Admin and super-admin protected operations
- API key generation and revocation

## Tech Stack

- Python 3.12+
- FastAPI
- Strawberry GraphQL
- SQLAlchemy
- PostgreSQL
- Redis
- PyJWT
- Pydantic / pydantic-settings
- Uvicorn

## Architecture

The codebase is organized around a fairly standard layered structure:

- `app/main.py`: FastAPI application bootstrap, CORS setup, webhook router, and GraphQL router
- `app/config/`: environment settings, database engines, and Redis clients
- `app/models/`: SQLAlchemy models
- `app/dto/`: Pydantic models used between layers
- `app/repositories/`: database access and persistence logic
- `app/services/`: token services, password hashing, cache helpers, rate limiting, and external integrations
- `app/graphql/`: schema composition, queries, mutations, inputs, types, permissions, and response helpers
- `app/routes/`: non-GraphQL HTTP routes
- `app/clients/`: outbound client integrations
- `app/utils/`: small utility helpers
- `tests/`: unit and async permission tests

## Main Functional Areas

### Authentication

The authentication flow is split into multiple steps:

1. `login` validates email and password.
2. A two-factor token and numeric code are generated and stored in Redis.
3. `verifyTwoFactor` consumes the temporary 2FA token and creates a session token.
4. Protected operations use the session token through the `session-id` header.

### API Key Protection

Some GraphQL operations also require an API key in the `Authorization` header:

- Format: `Authorization: Bearer <api-key>`

API keys are signed and stored in Redis with an expiration time. Protected resolvers validate the token before executing.

### Role-Based Authorization

The project defines three roles:

- `USER`
- `ADMIN`
- `SUPER_ADMIN`

Admin-only routes are enforced through Strawberry permission classes. Access is validated from the current session payload and checked against an allowlist of resolver names.

### Password Reset

The password reset flow also uses Redis-backed expiring tokens:

1. `forgotPassword` generates a reset token.
2. `resetPassword` validates and consumes that token.
3. The user password is updated after token verification.

### Webhook Validation

The `/webhook` route:

- Requires an `x-webhook-secret` header matching `WEBHOOK_SECRET`
- Expects a JSON payload with a `data` field
- Decodes the signed token using HS256
- Returns `204 No Content` when the payload is accepted

## Data Layer

The current database model includes a `users` table with:

- `userId`
- `name`
- `role`
- `email`
- `isDeleted`
- `password`
- `createdAt`
- `updatedAt`

Deletion is soft deletion in normal user flows: `delete_user` marks `isDeleted = True`.

There is also a repository helper to physically remove inactive users, but it is not exposed by the public API at the moment.

## Redis Usage

Redis is used as short-lived storage for:

- Sessions
- API keys
- Two-factor authentication codes
- Password reset tokens
- Rate limit counters

Expiration times currently defined in code:

- Session: 3 hours
- Two-factor authentication: 10 minutes
- Password reset: 15 minutes

## GraphQL Schema Summary

### Queries

- `getUser`
- `listUsers(page: Int = 1, limit: Int = 10)`
- `getByIdUser(userId: String!)`

### Mutations

- `create`
- `login`
- `verifyTwoFactor`
- `update`
- `delete`
- `forgotPassword`
- `resetPassword`
- `createApiKey`
- `createUserByAdmin`
- `updateUserByAdmin`
- `deleteUserByAdmin`
- `deleteApiKey`

### Key GraphQL Types

- `UserPublicType`
- `UserPrivateType`
- `SessionType`
- `TwoFactorAuthType`
- `ApiKeyType`
- `ApiResponseType`
- `ApiErrorType`

## Authentication and Headers

Depending on the resolver, the API may require one or both headers below:

- `Authorization: Bearer <session-token>`
- `api-key: <api-key>`

Resolver protection in practice:

- Public: `login`, `verifyTwoFactor`, `forgotPassword`, `resetPassword`
- API key only: `create`
- API key + session: `getUser`, `update`, `delete`
- Role-protected session routes: `listUsers`, `getByIdUser`, `createApiKey`, `createUserByAdmin`, `updateUserByAdmin`, `deleteUserByAdmin`, `deleteApiKey`

## Example GraphQL Flows

Sample operations already exist in [`auth.graphql`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/auth.graphql), which is a good starting point for manual testing.

Typical login flow:

1. Call `login` with email and password.
2. Read `token` and `number` from `TwoFactorAuthType`.
3. Call `verifyTwoFactor` with those values.
4. Store the returned `sessionId`.
5. Use `session-id` in subsequent protected calls.

## Environment Variables

Create a `.env` file in the project root and define the following values:

| Variable | Purpose |
|---|---|
| `REDIS_URL` | Redis connection string |
| `DATABASE_URL` | Synchronous PostgreSQL connection string |
| `DATABASE_URL_ASYNC` | Async PostgreSQL connection string |
| `CREATE_API_KEY` | Secret used to sign API keys |
| `PASSWORD_RESET_KEY` | Secret used to sign password reset tokens |
| `TWO_FACTOR_AUTH_KEY` | Secret used to sign 2FA tokens |
| `SESSION_KEY` | Secret used to sign sessions |
| `API_KEY` | API key used when calling the external notification system |
| `URL_NOTIFICATION_SYSTEM` | GraphQL endpoint for the notification service |
| `WEBHOOK_SECRET` | Shared secret used by `/webhook` |

Example:

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

## Installation

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
pip install -r requirements.txt
```

## Running Locally

Start the application with:

```bash
uvicorn app.main:app --reload
```

Default local URLs:

- App root: `http://localhost:8000/`
- GraphQL endpoint: `http://localhost:8000/graphql`
- OpenAPI docs: `http://localhost:8000/docs`

## Database Notes

This repository does not currently include migrations or seed scripts.

Before running the app, make sure:

- PostgreSQL is available
- Redis is available
- The required tables already exist in the database

## Caching and Performance Notes

The async SQLAlchemy engine is configured with:

- `pool_size=10`
- `max_overflow=20`
- `pool_recycle=3600`
- `pool_pre_ping=True`

There is also a Redis-backed user cache service used by admin list queries.

## External Notification Integration

The project contains an outbound GraphQL client for a notification system:

- `app/clients/notification_system_client.py`
- `app/services/queries/notification_system_service.py`

The mutation code already includes commented-out hooks for:

- registration emails
- password reset emails
- password change emails
- two-factor authentication emails

So the integration layer exists, but notification sending is currently disabled in the GraphQL mutation flow.

## Tests

The current test suite covers:

- timestamp defaults in the base model
- signed token decoding
- route protection behavior for admin and super-admin role checks

Run tests with:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Project Structure

```text
.
├── app
│   ├── clients
│   ├── config
│   ├── constants
│   ├── dto
│   ├── graphql
│   ├── models
│   ├── repositories
│   ├── routes
│   ├── services
│   └── utils
├── tests
├── auth.graphql
├── schema.graphql
├── pyproject.toml
└── requirements.txt
```

## Important Implementation Notes

- CORS is currently open to all origins.
- The GraphQL app does not define a custom context builder; permissions access the FastAPI request object from Strawberry's default integration.
- Redis keys are used as the token itself for session, API key, 2FA, and reset-token tracking.
- 2FA and password reset tokens are single-use because validation consumes them from Redis.
- User deletion is logical, not physical, in the exposed mutations.
- Creating users with the `SUPER_ADMIN` role is intentionally blocked in repository logic.

## Known Gaps

Based on the current repository state:

- There is no `.env.example` file.
- There are no migration files.
- There is no container setup.
- Rate limiting exists but is currently commented out in session permission execution.
- Some error messages and comments are still written in Portuguese in the application code.
- The root app title and some schema naming are still partially inconsistent (`Graphql`, `Graph API`, `graphql`).

## Useful Files

- [`app/main.py`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/app/main.py)
- [`schema.graphql`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/schema.graphql)
- [`auth.graphql`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/auth.graphql)
- [`app/repositories/user_repository.py`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/app/repositories/user_repository.py)
- [`app/graphql/mutations/user_mutation.py`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/app/graphql/mutations/user_mutation.py)
- [`app/graphql/mutations/admin_mutation.py`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/app/graphql/mutations/admin_mutation.py)
- [`app/graphql/permissions/session_permission.py`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/app/graphql/permissions/session_permission.py)
- [`app/graphql/permissions/routers_protects_permission.py`](/home/matheus-silva-oliveira/Área%20de%20trabalho/graph/app/graphql/permissions/routers_protects_permission.py)

## Summary

This repository is a compact authentication-oriented GraphQL backend with:

- JWT-based signed tokens
- Redis-backed temporary auth state
- PostgreSQL user persistence
- Role-based GraphQL protection
- Hooks for external notification delivery

It is a good base for authentication-heavy internal systems, admin panels, or service-to-service GraphQL backends that need API key and session-based protection together.
