#################### users.py ####################
import requests
import aiohttp
from load_env import Env

async def check_login(cookie) -> bool:
            # response = requests.post(Env.USER_CHECK_LOGIN_API, json=cookie, verify=False)
            # if response.status_code == 200:
            #     json_response = response.json()  # 解析 JSON
            #     return json_response.get('status') == "success"
    async with aiohttp.ClientSession() as session:
        async with session.post(Env.USER_CHECK_LOGIN_API, json=cookie, ssl=False) as response:
            if response.status == 200:
                json_response = await response.json()  # 解析 JSON
                return json_response.get('status') == "success"
            else:
                return False


# TODO
async def get_user_uuid(cookie) -> str:
    async with aiohttp.ClientSession() as session:
        
        async with session.post(Env.USER_GET_UUID_API, json=cookie, ssl=False) as response:
            if response.status == 200:
                json_response = await response.json()  # 解析 JSON
                return json_response.get('uuid')
            else:
                return ""