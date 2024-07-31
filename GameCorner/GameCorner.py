#################### GameCorner.py ####################
#################### 程式進入點 ####################
import asyncio
from pydantic import BaseModel
import uvicorn
from fastapi import Body, FastAPI, Request, HTTPException, requests
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

import games
import users
import utils

# Create an instance of the FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create an instance of the Jinja2Templates class
templates = Jinja2Templates(directory="templates")
DEFAULT_TITLE = "遊戲角落 - 榛果繽紛樂"
LOADER_IMG = f"data:image/png;base64,{utils.encode_local_image_to_base64('src/loader.png')}"

# Define your routes and handlers here

@app.get("/")
def home(request: Request):
    title = DEFAULT_TITLE
    return templates.TemplateResponse("index.html", {"request": request, "title": title, "loader": LOADER_IMG})

@app.post("/check_login_cookie")
def check_login_cookie(cookie: dict = Body(...)) -> bool:
    try:
        if cookie:
            return users.check_login(cookie=cookie)
    except:
        pass
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

class GameData(BaseModel):
    title: str
    description: str
    cover_image: str
    game_file: str  
@app.post("/post_game_data")
def post_game_data(game_data: GameData):
    try:
        games.post_game_data(game_data.title, game_data.description, game_data.cover_image, game_data.game_file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update_game_data")
def update_game_data(game_data: GameData):
    try:
        games.update_game_data(game_data.title, game_data.description, game_data.cover_image, game_data.game_file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @app.get("/game/{game_name}")
# def game_page(request: Request, game_name: str):
#     # get_game()
#     return templates.TemplateResponse("game.html", {"request": request, "game": game})




if __name__ == "__main__":
    uvicorn.run("GameCorner:app", host="127.0.0.1", port=4999, reload=True)