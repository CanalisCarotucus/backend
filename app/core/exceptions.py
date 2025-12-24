class BaseAppException(Exception):
    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str = None, status_code: int = None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code
        super().__init__(self.detail)


class UserNotFound(BaseAppException):
    status_code = 404

    def __init__(self, detail: str = "User not found"):
        super().__init__(detail=detail, status_code=self.status_code)


class PassportNotFound(BaseAppException):
    status_code = 404

    def __init__(self, detail: str = "Passport not found"):
        super().__init__(detail=detail, status_code=self.status_code)


class PassportAlreadyExists(BaseAppException):
    status_code = 400

    def __init__(self, detail: str = "Passport already exists"):
        super().__init__(detail=detail, status_code=self.status_code)


class UserAlreadyHasPassport(BaseAppException):
    status_code = 400

    def __init__(self, detail: str = "User already has passport"):
        super().__init__(detail=detail, status_code=self.status_code)


class PermissionDenied(BaseAppException):
    status_code = 403

    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail=detail, status_code=self.status_code)


class ValidationError(BaseAppException):
    status_code = 400

    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail=detail, status_code=self.status_code)

