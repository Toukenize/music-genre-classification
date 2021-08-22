from enum import Enum

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorCode(str, Enum):
    unauthorized = "unauthorized_error"
    postgres_error = "postgres_error"
    unhandled_error = "unhandled_error"
    file_type_error = "file_type_error"
    schema_error = 'input_data_schema_error'


class Error(BaseModel):
    errorCode: ErrorCode
    message: str

    def to_response(self, status_code):
        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": status_code,
                "info": self.dict()
            }
        )


class UnauthorizedException(Exception):
    pass


class DataSchemaException(Exception):
    pass


class FileTypeException(Exception):
    pass


class PostgresConnectionException(Exception):
    pass
