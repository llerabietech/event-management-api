from fastapi import FastAPI

from app.api import router

app = FastAPI(title="Event Manager", description="", version="1.0.0")

app.include_router(router.api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API! Перейдите на /docs для документации."}
