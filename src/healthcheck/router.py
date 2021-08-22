from fastapi import APIRouter

from ..config import settings

api_router = APIRouter(
    prefix=settings.API_PREFIX
)


@api_router.get("/healthcheck")
def healthcheck():
    """
    **Description**

    Healthcheck to confirm the service endpoint is running.
    """
    response = {
        "status": "success",
        "version": settings.API_VERSION,
        "name": settings.API_NAME
    }
    return response
