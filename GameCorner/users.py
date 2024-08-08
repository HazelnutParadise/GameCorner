#################### users.py ####################
import requests
import aiohttp
import urllib.parse
from load_env import Env

async def check_login(cookie) -> bool:
    decoded_cookie = urllib.parse.unquote(cookie)  # URI 解碼
    async with aiohttp.ClientSession() as session:
        async with session.post(Env.USER_CHECK_LOGIN_API, json=decoded_cookie, ssl=False) as response:
            if response.status == 200:
                json_response = await response.json()  # 解析 JSON
                return json_response.get('status') == "success"
            else:
                return False


async def get_user_uuid(cookie) -> str:
    decode_cookie = urllib.parse.unquote(cookie)  # URI 解碼
    data = decode_cookie
    data['whatToGet'] = ['allWithUUID']
    async with aiohttp.ClientSession() as session:
        async with session.post(Env.USER_GET_INFO_API, json=data, ssl=False) as response:
            if response.status == 200:
                json_response = await response.json()  # 解析 JSON
                return json_response.get('uuid')
            else:
                return ""