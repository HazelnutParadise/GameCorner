#################### utils.py ####################
import base64


def encode_image_to_base64(image_path: str) -> str:
    """将图片文件编码为 Base64 字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')