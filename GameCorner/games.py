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

def get_game_list(skip: int = 0, limit: int = 4) -> list:
    # 從api獲取遊戲數據
    result = requests.post(Env.DB_SQL_API, headers={
            'content-type': 'application/json'
        },
        data=json.dumps({
            "sql_statement": f"""
            SELECT id, name, description, cover_image FROM games order by id desc LIMIT {limit} OFFSET {skip};
            """, # 以 id 降冪排序，配合懶加載，可達成較新的遊戲在前
            'query_mode': True,
            'return_as_dict': True
        })
    )
    games = result.json()
    # games 是一個列表，每個元素是一個字典，代表一個遊戲
    # [
    # {
    #     'id': 1,
    #     'name': '遊戲1',
    #     'description': '這是遊戲1的描述',
    #     'cover_image': 'data:image/png;base64,xxxxxx'
    # },
    # ...
    # ]
   
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