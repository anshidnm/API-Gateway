from auth.routers import router as auth_router
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
