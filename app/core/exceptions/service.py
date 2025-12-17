from .base import AppException

class ServiceError(AppException):
    status_code = 400
    error_code = "SERVICE_ERROR"


class AuthError(ServiceError):
    error_code = "AUTH_ERROR"


class GoogleOAuthError(ServiceError):
    error_code = "GOOGLE_AUTH_ERROR"
