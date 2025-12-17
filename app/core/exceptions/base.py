class AppException(Exception):
    """Base exception untuk seluruh aplikasi"""
    status_code: int = 500
    error_code: str = "APP_ERROR"
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)