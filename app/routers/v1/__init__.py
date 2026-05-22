from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from strawberry.schema import Schema

from app.routers.v1.routers import auth_router
from app.routers.v1.graphql import query, mutation
from app.routers.v1.graphql.utils import get_context

router = APIRouter()

schema = Schema(
    query=query.Query,
    mutation=mutation.Mutation
)

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)

router.include_router(auth_router.router, prefix="/auth")
router.include_router(graphql_app, prefix="/graphql")


