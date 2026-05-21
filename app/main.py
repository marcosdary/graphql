from fastapi import FastAPI

import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.graphql.query import Query
from app.graphql.mutation import Mutation
from app.routers import v1
from app.graphql.utils import get_context

app = FastAPI(title="API do graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"]
)


schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation
)

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/v1/graphql")
app.include_router(v1.router, prefix="/v1")

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Graphql"
    }
