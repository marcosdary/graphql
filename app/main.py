from fastapi import FastAPI
import strawberry
from datetime import datetime, timezone
from strawberry.schema.config import StrawberryConfig
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.graphql.query import Query
from app.graphql.mutation import Mutation
from app.midlleware import ApiKeyMidlleware

from app.graphql.utils import get_context

app = FastAPI(title="API do graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"]
)

app.add_middleware(ApiKeyMidlleware)

schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation
)

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Graphql"
    }

