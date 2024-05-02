from fastapi import FastAPI, Header, HTTPException, File, UploadFile
from typing import Union

from fastapi import Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pycomcigan import get_school_code

import func
import requests
import os
import httpx

from dotenv import load_dotenv
load_dotenv(verbose=True)

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
    "/time/{where}",
    description="What time is now?\n/time/Asia/Seoul",
    status_code=200
)
async def time(where:str, response: Response):
    result = func.now(f"{where}")
    if result["success"] == False:
        return result
    return result


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


@app.get("/timetable/get/{school}/{grade}/{class_int}/{next}")
async def timetable_get(school:str, grade:int, class_int:int, next:int):
    return {"state": "Remaking"}

@app.get("/timetable/search/{school}")
async def timetable_search(school:str):
    return get_school_code(school)

@app.put("/deploy/web/{project}")
async def deploy_web_project(file: UploadFile, project:str, api_key:str):
    if api_key ==  os.getenv('SUPER_SECRET_TOKEN'):
        with open(f"/var/www/{project}.zip", "wb") as f:
            f.write(file.file.read())
        os.system(f"unzip -o /var/www/{project}.zip -d /var/www/{project}")
        return {"success": True}
    else:
        return {"success": False, "error": "이런거 하나 탈취하려니까 기분 좋아요?"}
        # 으악 퍼리다

#@app.get("/room")
#async def room():
#    url = "http://192.168.0.12:8000/"
#    async with httpx.AsyncClient() as client:
#        response = await client.get(url)
#        json_data = response.json()
#
#    return json_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=16)
