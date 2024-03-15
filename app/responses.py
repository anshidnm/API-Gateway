from fastapi.responses import JSONResponse
from fastapi import status


def bad_request(
    message: str = "Somthing went wrong",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    **kwargs,
):
    data = {
        "status": "FAILURE",
        "message": message
    }
    if kwargs:
        data.update(kwargs)
    return JSONResponse(
        data,
        status_code=status_code
    )