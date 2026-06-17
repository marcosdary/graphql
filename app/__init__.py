from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import routers

app = FastAPI(title="API do graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"]
)

app.include_router(routers.router, prefix="/api")

@app.get("/")
def index():
    return {
        "version": "5.3.5",
        "name": "Authenticator"
    }
