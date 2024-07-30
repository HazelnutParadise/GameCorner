#################### users.py ####################
import requests
from load_env import Env

def check_login(cookie) -> bool:
    if cookie:
        try:
            response = requests.post(Env.USER_CHECK_LOGIN_API, json=cookie, verify=False)
            if response.status_code == 200:
                json_response = response.json()  # 解析 JSON
                return json_response.get('status') == "success"
        except Exception as e:
            print(f"Error during request: {e}")
    return False
