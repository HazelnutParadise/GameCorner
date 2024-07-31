#################### games.py ####################
import json
import os
import requests
from load_env import Env
import utils

# 從api獲取遊戲列表
def get_game_list(skip: int = 0, limit: int = 4) -> list:
    result = requests.post(Env.DB_SQL_API, headers={
            'content-type': 'application/json'
        },
        data=json.dumps({
            "sql_statement": f"""
            SELECT id, name, description, cover_image FROM Games order by id desc LIMIT {limit} OFFSET {skip};
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


# TODO: 上傳遊戲到資料庫
# 本函數內容不正確
def post_game_data(title, description, cover_image, entry_file,  game_files) -> None:
    entry_file = utils.encode_base64(entry_file)

    # TODO: cover_image 需先處理為 bytes 的形式
    cover_image = utils.encode_base64(cover_image)

    # TODO: game_files 需先處理為 {file_name(str): file_content(base64)} 的形式

    game_data: dict = {
        "name": title,
        "description": description,
        "cover_image": cover_image,
        "entry_file": entry_file,
        "game_file": game_files
    }
    # 將遊戲數據發送到api
    requests.post(Env.DB_RECORD_API, headers={
        'content-type': 'application/json'
        },
        data=json.dumps({
            'records': game_data,
            'relation': "Games"
        }))

# TODO: 更新現有遊戲到資料庫
# 本函數內容不正確
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

