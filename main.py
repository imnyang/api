from fastapi import FastAPI, Header, HTTPException
from typing import Union

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import func
import httpx

app = FastAPI(
    title="api.imnyang.xyz",
    summary="imnyang's API",
    version="0.1.0",
    contact={
        "name": "💕",
        "url": "https://imnyang.xyz/about",
        "email": "api@imnyang.xyz",
    },
    license_info={
        "name": "GPL-3.0 license",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
    },
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    summary="Root",
    description="api.imnyang.xyz의 메인 페이지입니다.",
)
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get(
    "/time/{continent}/{country}",
    description="What time is now?",
)
async def time(continent:str, country:str):
    return func.now(f"{continent}/{country}")

@app.get("/get_client")
async def ip(request: Request, user_agent: Union[str, None] = Header(default=None)):
    client_host = request.client.host
    return {"success":True, "ip": client_host, "user_agent": user_agent}

@app.get("/room")
async def room():
    url = "http://192.168.0.12:8000/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        json_data = response.json()

    return json_data

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
