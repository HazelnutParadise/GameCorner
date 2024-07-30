#################### games.py ####################
import base64
import json
import os
import requests
from load_env import Env


def read_script(file_path: str) -> str:
    """读取文件并返回文件内容"""
    with open(file_path, 'r') as file:
        return file.read()

def get_game_data(skip: int = 0, limit: int = 4) -> list:
    # 從api獲取遊戲數據
    result = requests.post(Env.DB_SQL_API, headers={
            'content-type': 'application/json'
        },
        data=json.dumps({
            "sql_statement": f"SELECT * FROM games order by name asc LIMIT {limit} OFFSET {skip};",
            'query_mode': True,
            'return_as_dict': True
        })
    )
    games = result.json()
    games['title'] = games['name']
    # all_game_dirs = [file for file in os.listdir(GAMES_DIRECTORY) if os.path.isdir(os.path.join(GAMES_DIRECTORY, file))]
    # all_game_dirs = sorted(all_game_dirs)  # 现在按字母顺序排序
    # selected_game_dirs = all_game_dirs[skip:skip + limit]

    # games = []
    # for game_dir in selected_game_dirs:
    #     game_path = os.path.join(GAMES_DIRECTORY, game_dir)
    #     if os.path.isdir(game_path):
    #         metadata_path = os.path.join(game_path, "metadata.json")
    #         with open(metadata_path, 'r') as file:
    #             metadata = json.load(file)
    #         cover_image_path = os.path.join(game_path, metadata["cover_image"])
    #         if not os.path.exists(cover_image_path):
    #             cover_image_path = "src/default.webp"
    #         cover_image_base64 = encode_image_to_base64(cover_image_path)
    #         games.append({
    #             "title": metadata["title"],
    #             "description": metadata["description"],
    #             "cover_image": f"data:image/jpeg;base64,{cover_image_base64}"
    #         })
    return games

def post_game_data(title, description, cover_image, game_file) -> None:
    game_data: dict = {
        "title": title,
        "description": description,
        "cover_image": cover_image,
        "game_file": game_file
    }
    # 將遊戲數據發送到api
    requests.post(Env.DB_RECORD_API, headers={
        'content-type': 'application/json'
        },
        data=json.dumps({
            'records': game_data,
            'relation': "Games"
        }))

def update_game_data(title, description, cover_image, game_file) -> None:
    game_data: dict = {
        "title": title,
        "description": description,
        "cover_image": cover_image,
        "game_file": game_file
    }
    # 將遊戲數據發送到api
    requests.put(Env.DB_RECORD_API, headers={
        'content-type': 'application/json'
        }, data=json.dumps({
            'conditions': {}, # TODO!
            'records': game_data,
            'relation': "Games"
        }))

def encode_image_to_base64(image_path: str) -> str:
    """将图片文件编码为 Base64 字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')