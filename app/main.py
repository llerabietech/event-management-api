from fastapi import FastAPI

from app.api import router
from app.core.error_handlers import register_error_handlers
from app.middleware import register_middleware

app = FastAPI(title="Event Manager", description="", version="1.0.0")

register_error_handlers(app)
register_middleware(app)
app.include_router(router.api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API! Перейдите на /docs для документации."}
