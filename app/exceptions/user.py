from app.exceptions.base import ConflictError, NotFoundError


class UserNotFoundError(NotFoundError):
    error_code = "USER_NOT_FOUND"

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")


class UserAlreadyExistsError(ConflictError):
    error_code = "USER_ALREADY_EXISTS"

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User {username} already exists")


class UserNotAuthorized(Exception):
    error_code = "USER_NOT_AUTHORIZED"
    status_code = 401

    def __init__(self):
        super().__init__("User is not authorized")
