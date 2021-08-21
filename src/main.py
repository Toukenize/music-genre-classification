import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse

from config import settings
from errors import Error, ErrorCode, FileTypeException, UnauthorizedException
from src import classifier, healthcheck

app = FastAPI()
app.include_router(healthcheck.router.api_router)
app.include_router(classifier.router.api_router)


@app.get('/')
def index():
    return RedirectResponse(settings.API_PREFIX + '/healthcheck')


@app.exception_handler(UnauthorizedException)
def unauthorized_exception(_request: Request, error: UnauthorizedException):
    error = Error(
        message=str(error),
        errorCode=ErrorCode.unauthorized
    )
    logging.error(f'{ErrorCode.unauthorized}; {str(error)}')
    return error.to_response(status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(FileTypeException)
def file_type_exception(_request: Request, error: FileTypeException):

    error = Error(
        message=str(error),
        errorCode=ErrorCode.file_type_error
    )
    logging.error(f'{ErrorCode.file_type_error}; {str(error)}')
    return error.to_response(status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(Exception)
def base_exception(_request: Request, error: Exception):
    error = Error(
        message=str(error),
        errorCode=ErrorCode.unhandled_error
    )
    logging.error(f'{ErrorCode.unhandled_error}; {str(error)}')
    return error.to_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
