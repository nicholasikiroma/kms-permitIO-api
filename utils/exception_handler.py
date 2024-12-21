from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError


def jsend_response(status: str, message: str = None, data: dict = None):
    """Helper function to create a JSend-compliant response."""
    response = {"status": status}
    if message:
        response["message"] = message
    if data:
        response["data"] = data
    return response


async def server_exception_handler(request: Request, exc: Exception):
    """General exception handler for unexpected errors."""
    return JSONResponse(
        status_code=500,
        content=jsend_response(
            status="error",
            message="An internal server error occurred. Please try again later.",
        ),
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handles validation errors."""
    errors = {err["loc"][1]: err["msg"] for err in exc.errors()}
    return JSONResponse(
        status_code=422,
        content=jsend_response(
            status="fail",
            data=errors,
        ),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles HTTP exceptions."""
    status_code = exc.status_code
    if status_code == 422:  # Handle validation errors separately
        return await validation_exception_handler(request, exc)

    return JSONResponse(
        status_code=status_code,
        content=jsend_response(
            status="fail",
            message=exc.detail if exc.detail else "HTTP error occurred",
        ),
    )
