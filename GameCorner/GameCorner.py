#################### GameCorner.py ####################
#################### 程式進入點 ####################
import asyncio
import random
import secrets
from pydantic import BaseModel
import uvicorn
from fastapi import Body, FastAPI, File, Form, Request, HTTPException, UploadFile
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

import games
import users
import utils
from Renderer import Renderer
from load_env import Env

# Create an instance of the FastAPI app
app = FastAPI(docs_url=None, redoc_url=None)
key_length = random.randint(32, 64)
SECRET_KEY = secrets.token_urlsafe(key_length)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create an instance of the Jinja2Templates class
templates = Jinja2Templates(directory="templates")

# Define constants
SITE_NAME = "遊戲角落"
DEFAULT_TITLE = f"{SITE_NAME} - 榛果繽紛樂"
SITE_LOGO = f"data:image/png;base64,{utils.encode_local_image_to_base64('src/logo_resized.png')}"
LOADER_IMG = f"data:image/png;base64,{utils.encode_local_image_to_base64('src/loader.png')}"

# Define your routes and handlers here

@app.get("/")
async def home(request: Request):
    title = DEFAULT_TITLE
    return templates.TemplateResponse("index.html", {"request": request, "title": title, "loader": LOADER_IMG})

@app.post("/check_login_cookie")
async def check_login_cookie(request: Request, cookie: dict = Body(...)) -> bool:
    if cookie:
        if await users.check_login(cookie=cookie):
            request.session['verified_login'] = True
            return True
    request.session['verified_login'] = False
    return False

@app.post("/load_games_list")
async def load_games_list(request: Request) -> list:
    # await asyncio.sleep(5)
    try:
        # 使用 await 等待异步方法 json() 的结果
        data = await request.json()
        skip = data['skip']
        limit = data['limit']
        # 假设 get_game_data 是一个同步函数，需要适当的处理数据获取逻辑
        games_list = games.get_game_list(skip=skip, limit=limit)
        return games_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# TODO: 前端表單加上author_id
@app.post("/game")
async def post_game_data(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    author_id: str = Form(...),
    cover_image: UploadFile = File(...),
    entry_file: UploadFile = File(...),
    game_files: list[UploadFile] = File(...)
):
    if not request.session['verified_login']:
        raise HTTPException(status_code=401, detail="Unauthorized")
    cover_image = cover_image.read()
    entry_file = entry_file.read().decode("utf-8")
    game_files = {file.filename: file.read() for file in game_files}
    for key, value in game_files.items():
        if key.endswith(".html") or key.endswith(".*js") or key.endswith(".css"):
            game_files[key] = value.decode("utf-8")
    err = await games.post_game_data(name, description, author_id, cover_image, entry_file, game_files)
    if err:
        raise HTTPException(status_code=400, detail=err)

@app.put("/game/{game_id}")
def update_game_data(
    request: Request,
    game_id: int,
    name: str = Form(...),
    description: str = Form(...),
    cover_image: UploadFile = File(...),
    entry_file: UploadFile = File(...),
    game_files: list[UploadFile] = File(...)
):
    if not request.session['verified_login']:
        raise HTTPException(status_code=401, detail="Unauthorized")
    cover_image = cover_image.read()
    entry_file = entry_file.read().decode("utf-8")
    game_files = {file.filename: file.read() for file in game_files}
    for key, value in game_files.items():
        if key.endswith(".html") or key.endswith(".*js") or key.endswith(".css"):
            game_files[key] = value.decode("utf-8")
    err = games.update_game_data(game_id, name, description, cover_image, entry_file, game_files)
    if err:
        raise HTTPException(status_code=400, detail=err)

@app.get("/game/{game_id}")
async def game_page(request: Request, game_id: int):
    game = await games.get_game(game_id)
    if not game:
        return HTTPException(status_code=404, detail="Game not found.")
    game_name = game.get("name")
    entry_file = game.get("entry_file")
    resources = game.get("game_files")
    resources_url = f"/game/resource/{game_id}"
    rendered_game = Renderer.render_html(entry_file, resources, backend_url=resources_url, only_render_between_GAME_tags=True)
    return templates.TemplateResponse("game.html", {"request": request, "game_title": game_name, "site_name": SITE_NAME, "site_logo": SITE_LOGO, "rendered_game": rendered_game})

@app.delete("/game/{game_id}")
def delete_game(request: Request, game_id: int):
    if not request.session.get('verified_login'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    err = games.delete_game(game_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return HTTPException(status_code=200, detail="Game deleted successfully.")

@app.get("/game/resource/{game_id}/{file_name}")
async def game_resource(game_id: int, file_name: str):
    return await games.get_game_resource(game_id, file_name)


if __name__ == "__main__":
    uvicorn.run("GameCorner:app", host="127.0.0.1", port=4999, reload=True)