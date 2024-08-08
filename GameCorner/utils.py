#################### utils.py ####################
import base64
import re


# 將圖片檔編碼為 Base64
def encode_local_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return encode_base64(image_file.read())


# 編碼為 Base64
def encode_base64(content: bytes) -> str:
    return base64.b64encode(content).decode()


# 解碼 Base64
def decode_base64(content: str) -> bytes:
    return base64.b64decode(content)

# 清理路徑
def clean_path(path):
    # 去除所有前缀，包括 .、./ 和 /
    return re.sub(r'^[./]+', '', path)


