from fastapi import FastAPI, Header
from typing import Union

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import func
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/time/kst")
async def time():
    return func.kst_now()

@app.get("/get_client")
async def ip(request: Request, user_agent: Union[str, None] = Header(default=None)):
    client_host = request.client.host
    return {"ip": client_host, "user_agent": user_agent}

@app.get("/room")
async def room():
    url = "http://192.168.0.12:8000/"
    response = requests.get(url)
    json_data = response.json()

    return json_data

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
