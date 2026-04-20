import logging
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.graphql.query import Query
from app.graphql.mutation import Mutation
from app.routes import webhook_route

app = FastAPI(title="API do graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"],
)

app.include_router(webhook_route.router)

schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[])

graphql_app = GraphQLRouter(schema=schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Graphql"
    }

