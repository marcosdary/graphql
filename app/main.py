from fastapi import FastAPI
import strawberry
from datetime import datetime, timezone
from strawberry.schema.config import StrawberryConfig
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.graphql.query import Query
from app.graphql.mutation import Mutation
from app.midlleware import ApiKeyMidlleware
from app.graphql.extensions import ValidateExtension
from app.graphql.utils import get_context
from app.routes import webhook_route

app = FastAPI(title="API do graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"],
)

app.add_middleware(ApiKeyMidlleware)

app.include_router(webhook_route.router)

schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation, 
    extensions=[ValidateExtension],
    config=StrawberryConfig(
        scalar_map={
            datetime: strawberry.scalar(
                name="DateTime",
                serialize=lambda value: int(value.timestamp()),
                parse_value=lambda value: datetime.fromisoformat(
                    int(value), timezone.utc
                )
            )
        }
    )
)

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Graphql"
    }

