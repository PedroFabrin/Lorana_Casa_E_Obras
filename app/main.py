from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.routes import router

app = FastAPI(
    title="Lorana Casa e Obras",
    version="1.0.0",
    swagger_ui_init_oauth={},
)

app.include_router(router)
