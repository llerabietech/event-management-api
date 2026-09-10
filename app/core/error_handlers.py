"""Модуль регистрации обработчиков исключений приложения.

Определяет централизованные обработчики ошибок для FastAPI приложения.
Все ошибки возвращаются в едином формате:

{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable message",
        "details": [...]  # опционально
    }
}

Обрабатываемые типы исключений:
- AppException — кастомные ошибки приложения (404, 403, 409 и т.д.)
- HTTPException — стандартные ошибки FastAPI/Starlette
- RequestValidationError — ошибки валидации входных данных (422)
- Exception — необработанные ошибки (500)
"""
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppException

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """Регистрирует все обработчики исключений в приложении.
    Вызывается один раз при инициализации приложения

    Args:
        app: Экземпляр FastAPI приложения,
            к которому привязываются обработчики.

    Returns:
        None. Обработчики регистрируются через декораторы
        ``@app.exception_handler``.
    """
    @app.exception_handler(AppException)
    async def app_error_handler(request: Request, exc: AppException):
        """Обрабатывает кастомные исключения приложения.

        Args:
            request: HTTP-запрос, вызвавший исключение.
            exc: Экземпляр ``AppException`` с атрибутами
                ``status_code``, ``error_code`` и ``message``.

        Returns:
            JSONResponse со статус-кодом из ``exc.status_code``
            и телом в едином формате ошибок.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                }
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Обрабатывает стандартные HTTP-исключения FastAPI.

        Args:
            request: HTTP-запрос, вызвавший исключение.
            exc: Экземпляр ``HTTPException`` с атрибутами
                ``status_code``, ``detail`` и опциональным ``headers``.

        Returns:
            JSONResponse со статус-кодом из ``exc.status_code``
            и телом в едином формате ошибок.
            Заголовки из ``exc.headers`` передаются в ответ.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "HTTP_ERROR",
                    "message": exc.detail,
                }
            },
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        """Обрабатывает ошибки валидации входных данных.

        Args:
            request: HTTP-запрос, вызвавший ошибку валидации.
            exc: Экземпляр ``RequestValidationError`` со списком
                ошибок валидации в ``exc.errors()``.

        Returns:
            JSONResponse со статус-кодом 422
            и детальным описанием ошибок валидации.
        """
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request data is invalid",
                    "details": jsonable_encoder(exc.errors()),
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        """Обрабатывает все необработанные исключения.

        Args:
            request: HTTP-запрос, вызвавший исключение.
            exc: Экземпляр необработанного исключения.

        Returns:
            JSONResponse со статус-кодом 500
            и обезличенным сообщением об ошибке.
        """
        logger.exception(
            "Unhandled error: %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Internal server error",
                }
            },
        )
