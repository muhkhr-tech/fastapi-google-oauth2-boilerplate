from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from app.core.exceptions.base import AppException
from app.api.responses import error_response

logger = logging.getLogger(__name__)

def register_exception_handlers(app):
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.exception("Application error occurred")

        print(exc,'nihbos')

        return error_response(
            message=exc.message,
            status_code=exc.status_code,
            error_code=getattr(exc, "error_code", "APP_ERROR")
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")

        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "Terjadi kesalahan pada server"
            }
        )
