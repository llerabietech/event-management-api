class AppError(Exception):
    status_code = 500
    error_code = "INTERNAL_ERROR"
    message = "Internal server error"

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message


class AppException(Exception):
    status_code = 400
    error_code = "BAD_REQUEST"
    message = "Application error"

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message


class NotFoundError(AppException):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Resource not found"


class ConflictError(AppException):
    status_code = 409
    error_code = "CONFLICT"
    message = "Resource already exists"


class PermissionDeniedError(AppException):
    status_code = 403
    error_code = "PERMISSION_DENIED"
    message = "Permission denied"
