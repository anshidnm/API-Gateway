from auth.routers import router as auth_router
from gateway.services import CHAT_SERVICE
from gateway.request import APIGateway
from gateway.routers import router as api_gateway
from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from responses import bad_request

import config
import os


app = FastAPI(title="API Gateway & Authentication")

app.include_router(auth_router, prefix="/auth")
app.include_router(api_gateway, prefix="/api")


@app.get(config.MEDIA_URL+"{location:path}", tags=["Media"])
async def media_files(location: str):
    try:
        root = f"/{config.MEDIA_ROOT.strip('/')}/"
        if os.path.isfile(root+location):
            return FileResponse(root+location)
        return bad_request("File not found", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return bad_request(str(e))


@app.get("/room", tags=["Chat"])
async def room_list(
    user_id: int,
    skip: int = 0,
    limit: int = 10
):
    api_url = CHAT_SERVICE.api_url + "/room"
    api = APIGateway(
        api_url,
        "get",
        params={
            "user_id": user_id,
            "skip": skip,
            "limit": limit
        }
    )
    res = await api.make_request()
    return res


@app.get("/external-media/{location:path}", tags=["Media Files Fom Other services"])
async def media_files(
    location: str
):
    api_url = CHAT_SERVICE.api_url + f"/media/{location}"
    api = APIGateway(
        api_url,
        "get",
    )
    res = await api.make_request()
    return res