from pydantic import BaseModel, Field, ConfigDict


class ErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    detail: str = Field(..., description="Описание ошибки")
    status_code: int = Field(..., description="HTTP статус код")


class ValidationErrorResponse(ErrorResponse):
    detail: str = Field(default="Validation error", description="Описание ошибки валидации")
    status_code: int = Field(default=400, description="HTTP статус код")


class NotFoundErrorResponse(ErrorResponse):
    detail: str = Field(default="Resource not found", description="Описание ошибки")
    status_code: int = Field(default=404, description="HTTP статус код")


class PermissionDeniedErrorResponse(ErrorResponse):
    detail: str = Field(default="Permission denied", description="Описание ошибки доступа")
    status_code: int = Field(default=403, description="HTTP статус код")


class BadRequestErrorResponse(ErrorResponse):
    detail: str = Field(default="Bad request", description="Описание ошибки запроса")
    status_code: int = Field(default=400, description="HTTP статус код")


class InternalServerErrorResponse(ErrorResponse):
    detail: str = Field(default="Internal server error", description="Описание внутренней ошибки")
    status_code: int = Field(default=500, description="HTTP статус код")

