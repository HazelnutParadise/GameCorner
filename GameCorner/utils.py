#################### utils.py ####################
import base64
import re

# 將圖片檔編碼為 Base64
def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return encode_base64(image_file.read())

# 編碼為 Base64
def encode_base64(content: str) -> base64:
    return base64.b64encode(content.encode('utf-8')).decode('utf-8')

# 解碼 Base64
def decode_base64(content: base64) -> str:
    return base64.b64decode(content).decode('utf-8')

# 清理路徑
def clean_path(path):
    # 去除所有前缀，包括 .、./ 和 /
    return re.sub(r'^[./]+', '', path)

# 將 HTML 內容中的資源標籤替換為嵌入(js/css)或後端連結(img)
def process_html_tags(html_content, resources, backend_url):
    # 處理 <link> 標籤
    link_regex = re.compile(r'<link\s+[^>]*href="([^"]+)"[^>]*>')
    html_content = link_regex.sub(lambda match: replace_link_tag(match, resources), html_content)

    # 處理 <script> 標籤
    script_regex = re.compile(r'<script\s+[^>]*src="([^"]+)"[^>]*></script>')
    html_content = script_regex.sub(lambda match: replace_script_tag(match, resources), html_content)

    # 處理 <img> 標籤
    img_regex = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*>')
    html_content = img_regex.sub(lambda match: replace_img_tag(match, resources), html_content)

    # 替換 <link> 標籤的函數
    def replace_link_tag(match, resources):
        href = clean_path(match.group(1))
        resource = next((res for res in resources if res.name == href), None)
        if resource:
            decoded_content = decode_base64(resource.content)
            decoded_content = replace_css_imports(decoded_content, resources)
            return f'<style>{decoded_content}</style>'
        return match.group(0)

    # 替換 <script> 標籤的函數
    def replace_script_tag(match, resources):
        src = clean_path(match.group(1))
        resource = next((res for res in resources if res.name == src), None)
        if resource:
            decoded_content = decode_base64(resource.content)
            decoded_content = replace_js_imports(decoded_content, resources)
            return f'<script>{decoded_content}</script>'
        return match.group(0)

    # 替換 <img> 標籤的函數
    def replace_img_tag(match, resources):
        src = clean_path(match.group(1))
        resource = next((res for res in resources if res.name == src), None)
        if resource:
            return f'<img src="{backend_url}/{resource.name}" />'
        return match.group(0)

    return html_content


# 將 CSS 內容中的 @import 替換為嵌入內容
def replace_css_imports(content, resources):
    import_regex = re.compile(r'@import\s+["\'](.+?)["\'];')
    matches = import_regex.findall(content)
    for match in matches:
        import_path = clean_path(match)
        imported_resource = next((res for res in resources if res.name == import_path), None)
        if imported_resource:
            imported_content = decode_base64(imported_resource.content)
            content = content.replace(f'@import "{match}";', imported_content)
            content = replace_css_imports(content, resources)  # 遞迴替換
    return content

# 將 JavaScript 內容中的 import/require 替換為嵌入內容或後端連結
def replace_js_imports(content, resources, backend_url):
    import_regex = re.compile(r'import\s+[\s\S]*?\s+from\s+["\'](.+?)["\'];|require\s*\(\s*["\'](.+?)["\']\s*\)')
    matches = import_regex.findall(content)
    for match in matches:
        import_path = clean_path(match[0] or match[1])
        imported_resource = next((res for res in resources if res.name == import_path), None)
        if imported_resource:
            if not import_path.endswith(('.js', '.mjs', '.cjs')):
                # 如果是非js資源，則替換為後端連結
                content = content.replace(match[0] or match[1], f'{backend_url}/{imported_resource.name}')
            else:
                imported_content = decode_base64(imported_resource.content)
                content = content.replace(match[0] or match[1], imported_content)
                content = replace_js_imports(content, resources)  # 遞迴替換
    return content