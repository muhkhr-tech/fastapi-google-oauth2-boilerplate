class AppException(Exception):
    """Base exception untuk seluruh aplikasi"""
    status_code: int = 500
    error_code: str = "APP_ERROR"
    
    def __init__(self, status_code: int, message: str):
        self.message = message
        self.status_code = status_code
        super().__init__(status_code, message)


class ServiceError(AppException):
    status_code: int = 400
    error_code: str = "SERVICE_ERROR"


class GoogleOAuthError(ServiceError):
    status_code: int = 400
    error_code: str = "GOOGLE_AUTH_ERROR"

class AuthError(ServiceError):
    error_code: str = "AUTH_ERROR"
    status_code: int = 400

