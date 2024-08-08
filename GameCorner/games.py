#################### games.py ####################
import json
import os
import aiohttp
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
    resultJson = result.json()
    games = resultJson.get('result')

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

async def get_game_list_by_author(author_id: int) -> list:
    async with aiohttp.ClientSession() as session:
        url = f"{Env.DB_RECORD_API}?relation=Games&conditions_str={json.dumps({'author_id': author_id})}"
        async with session.get(url, headers={
            'content-type': 'application/json'
        }) as response:
            resultJson = await response.json() if response.status == 200 else None
            games = resultJson.get('result') if resultJson else None
            return games


# 從api獲取單個遊戲
async def get_game(id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        url = f"{Env.DB_SQL_API}?relation=Games&conditions_str={json.dumps({'id': id})}&return_as_dict=True"
        async with session.get(Env.DB_RECORD_API, headers={
            'content-type': 'application/json'
        }) as response:
            game = await response.json() if response.status == 200 else None
            return game
        
# 從api獲取遊戲依賴資源
async def get_game_resource(id: int, file_name: str) -> bytes | None:
    async with aiohttp.ClientSession() as session:
        url = f"{Env.DB_SQL_API}?relation=Games&conditions_str={json.dumps({'id': id})}&to_query={json.dumps(['game_files'])}"
        async with session.get(Env.DB_RECORD_API, headers={
            'content-type': 'application/json'
        }) as response:
            files = await response.json() if response.status == 200 else None
            if files:
                files = files[0]
                # 這裡的 files 是一個字典，key 是檔案名，value 是 base64 編碼的檔案內容
                file_content_to_return = files.get(file_name)
                if file_content_to_return:
                    return utils.decode_base64(file_content_to_return)
            return None

# 上傳遊戲到資料庫
async def post_game_data(title, description, author_id, cover_image, entry_file,  game_files) -> None | str:
    entry_file = utils.encode_base64(entry_file)
    cover_image = utils.encode_base64(cover_image)
    game_files = {key: utils.encode_base64(value) for key, value in game_files.items()}

    game_data: dict = {
        "name": title,
        "description": description,
        "author_id": author_id,
        "cover_image": cover_image,
        "entry_file": entry_file,
        "game_file": game_files
    }
    # 將遊戲數據發送到api
    result = requests.post(Env.DB_RECORD_API, headers={
        'content-type': 'application/json'
        },
        data=json.dumps({
            'records': game_data,
            'relation': "Games"
        }))
    result = result.json()
    if result.get('status') != "success":
        return result.get('message')
    else:
        return None


# 更新現有遊戲到資料庫
def update_game_data(id, name=None, description=None, cover_image=None, entry_file=None, game_files=None) -> None | str:
    entry_file = utils.encode_base64(entry_file) if entry_file else None
    cover_image = utils.encode_base64(cover_image) if cover_image else None
    game_files = {key: utils.encode_base64(value) for key, value in game_files.items()} if game_files else None
    game_data: dict = {
        "name": name if name else None,
        "description": description if description else None,
        "cover_image": cover_image if cover_image else None,
        "entry_file": entry_file if entry_file else None,
        "game_file": game_files if game_files else None
    }

    # 將遊戲數據發送到api
    result = requests.put(Env.DB_RECORD_API, headers={
        'content-type': 'application/json'
        }, data=json.dumps({
            'conditions': {'id': id},
            'records': game_data,
            'relation': "Games"
        }))
    
    result = result.json()
    if result.get('status') != "success":
        return result.get('message')
    return None


# 刪除遊戲
def delete_game(id) -> None | str:
    condition = {
        "id": id
    }
    condition_str = json.dumps(condition)

    url = f"{Env.DB_RECORD_API}?relation=Games&conditions_str={condition_str}"

    # 將遊戲數據發送到api
    result = requests.delete(url, headers={
        'content-type': 'application/json'
        })
    
    result = result.json()
    if result.get('status') != "success":
        return result.get('message')
    return None