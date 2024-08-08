#################### load_env.py ####################
from dotenv import load_dotenv
import os

# 載入 .env 文件
load_dotenv()
# 設定環境變數

class Env:
    DB_SQL_API = os.getenv("DB_SQL_API")
    DB_RECORD_API = os.getenv("DB_RECORD_API")
    USER_CHECK_LOGIN_API = os.getenv("USER_CHECK_LOGIN_API")
    BACKEND_URL = os.getenv("BACKEND_URL")
    USER_GET_INFO_API = os.getenv("USER_GET_INFO_API")