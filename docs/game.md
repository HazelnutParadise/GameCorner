# Handling Game Files 遊戲程式檔的處理
### The files of the game programs will be classified into TWO parts and saved in the database.<br/>遊戲的程式碼會分為兩類並儲存在資料庫中。

## 1. Entry File 入口檔（程式進入點）
The entry file is an HTML file that contains the entry point of a game program and a pair of (and only **ONE** pair of) `<GAME>` `</GAME>` tags, as shown below:<br/>
入口檔是一個帶有遊戲程式入口點，並包含 **僅一對** `<GAME>` `</GAME>` 標籤的 HTML 檔案，長得像下面這樣：
```html
<GAME>
  <!-- The code of the game, usually <canvas> or <div> -->
  <!-- 遊戲的程式碼，通常是一個 <canvas> 或 <div> 元素 -->
</GAME>
```
Entry files will be converted into **base64**, and saved directly into the database as **BLOB** items.<br/>
入口檔會轉換成 **base64** 格式並直接以 **BLOB** 的形式存入資料庫。

## 2. Other Game Files 其他遊戲檔案
Other game files, such as JavaScript or CSS, will be converted into a **Python dictionary** as follows:<br/>
其他遊戲檔案（如 JavaScript 或 CSS）會被轉換成如下所示的 **Python 字典**：
```py
{
  file_name(string): file_content(base64),
  # ...other files
  # ...更多
}
```

# Game Page 遊戲頁面
GameCorner have to find the `<GAME>` tag in **entry files**, and put the content between `<GAME>` and `</GAME>` in the `<div>` on the ***game page***.<br/>
GameCorner 必須在 **入口檔案** 中找到 `<GAME>` 標籤，並將 `<GAME>` 和 `</GAME>` 之間的內容放在 ***遊戲頁面*** 上的 `<div>` 中。
