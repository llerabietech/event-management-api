from app.exceptions import AppException


class AuthenticationError(AppException):
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"
    message = "Authentication failed"


class InvalidCredentialsError(AuthenticationError):
    error_code = "INVALID_CREDENTIALS"
    message = "Incorrect username or password"


class AccessTokenInvalidError(AuthenticationError):
    error_code = "ACCESS_TOKEN_INVALID"
    message = "Access token is invalid or expired"


class RefreshTokenInvalidError(AuthenticationError):
    error_code = "REFRESH_TOKEN_INVALID"
    message = "Refresh token is invalid or expired"