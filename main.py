from fastapi import FastAPI, Header, HTTPException, File, UploadFile
from typing import Union

from fastapi import Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import func
import requests
import os
import aiofiles

from dotenv import load_dotenv
load_dotenv(verbose=True)

app = FastAPI(
    title="api.imnyang.xyz",
    summary="imnyang's API",
    version="1.0.0",
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
    "/weather/{city}/{units}",
    summary="openweathermap",
    description="This is Weather",
)
async def weather(city:str, units:str):
    return func.get_weather(city, units)

@app.post("/website/send")
async def send(request: Request, message:str):
    result = requests.post("https://discord.com/api/webhooks/1224283449427497011/U5EnBi0FZ9UB1c6fc-Je1vdgCj8mvRqJLWUZjN588_qxegggpIDTWG4ciiMNyayR1R6K", json = {
        "content" : message,
        "username" : request.client.host
    })
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {"success": False, "error": err}

    else:
        return {"success": True}


@app.get("/get_client")
async def ip(request: Request, user_agent: Union[str, None] = Header(default=None)):
    client_host = request.client.host
    return {"success":True, "ip": client_host, "user_agent": user_agent}

@app.get("/neis/search/{school}")
async def search_school(school:str):
    url = f'https://open.neis.go.kr/hub/schoolInfo?Type=json&SCHUL_NM={school}'

    # GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    # 응답이 성공적이면 JSON 데이터를 추출
    if response.status_code == 200:
        data = response.json()

        # 학교 이름을 추출
        school_names = []

        # JSON 데이터에서 학교 이름 추출
        for item in data.get('schoolInfo', [])[1].get('row', []):
            school_name = item.get('SCHUL_NM', '')
            if school_name:
                school_names.append(school_name)

        # 학교 이름 리스트를 출력
        return {"success": True, "school_names": school_names}
    else:
        return {"success": False, "error": response.text}

@app.put("/discord/save")
async def save(file: UploadFile):
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    return {"filename": file.filename, "file_size": len(content)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=16)
