import re

import utils


class Renderer:

    # resources 應該長這樣
    # resources = [
    #     {
    #         'name': 'styles.css',
    #         'content': base64.b64encode(b'body { background: red; }').decode('utf-8')
    #     },
    #     {
    #         'name': 'script.js',
    #         'content': base64.b64encode(b'console.log("Hello, World!");').decode('utf-8')
    #     },
    #     {
    #         'name': 'image.png',
    #         'content': base64.b64encode(b'binary image data').decode('utf-8')
    #     }
    # ]

    @classmethod
    def render_html(cls, html_content, resources: list[dict] = None, backend_url: str = ""):
        html_content = utils.decode_base64(html_content)
        if not resources:
            return html_content
        # 處理 HTML 內容中的資源標籤
        html = cls.__process_html_tags(html_content, resources, backend_url)
        return html

    # 將 HTML 內容中的資源標籤替換為嵌入(js/css)或後端連結(img)
    @classmethod
    def __process_html_tags(cls, html_content, resources, backend_url):
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
            href = utils.clean_path(match.group(1))
            resource = next((res for res in resources if res.name == href), None)
            if resource:
                decoded_content = utils.decode_base64(resource.content)
                decoded_content = cls.__replace_css_imports(decoded_content, resources)
                return f'<style>{decoded_content}</style>'
            return match.group(0)

        # 替換 <script> 標籤的函數
        def replace_script_tag(match, resources):
            src = utils.clean_path(match.group(1))
            resource = next((res for res in resources if res.name == src), None)
            if resource:
                decoded_content = utils.decode_base64(resource.content)
                decoded_content = cls.__replace_js_imports(decoded_content, resources)
                return f'<script>{decoded_content}</script>'
            return match.group(0)

        # 替換 <img> 標籤的函數
        def replace_img_tag(match, resources):
            src = utils.clean_path(match.group(1))
            resource = next((res for res in resources if res.name == src), None)
            if resource:
                return f'<img src="{backend_url}/{resource.name}" />'
            return match.group(0)

        return html_content


    # 將 CSS 內容中的 @import 替換為嵌入內容
    @classmethod
    def __replace_css_imports(cls, content, resources):
        import_regex = re.compile(r'@import\s+["\'](.+?)["\'];')
        matches = import_regex.findall(content)
        for match in matches:
            import_path = utils.clean_path(match)
            imported_resource = next((res for res in resources if res.name == import_path), None)
            if imported_resource:
                imported_content = utils.decode_base64(imported_resource.content)
                content = content.replace(f'@import "{match}";', imported_content)
                content = cls.__replace_css_imports(content, resources)  # 遞迴替換
        return content


    # 將 JavaScript 內容中的 import/require 替換為嵌入內容或後端連結
    @classmethod
    def __replace_js_imports(cls, content, resources, backend_url):
        import_regex = re.compile(r'import\s+[\s\S]*?\s+from\s+["\'](.+?)["\'];|require\s*\(\s*["\'](.+?)["\']\s*\)')
        matches = import_regex.findall(content)
        for match in matches:
            import_path = utils.clean_path(match[0] or match[1])
            imported_resource = next((res for res in resources if res.name == import_path), None)
            if imported_resource:
                if not import_path.endswith(('.js', '.mjs', '.cjs')):
                    # 如果是非js資源，則替換為後端連結
                    content = content.replace(match[0] or match[1], f'{backend_url}/{imported_resource.name}')
                else:
                    imported_content = utils.decode_base64(imported_resource.content)
                    content = content.replace(match[0] or match[1], imported_content)
                    content = cls.__replace_js_imports(content, resources)  # 遞迴替換
        return content