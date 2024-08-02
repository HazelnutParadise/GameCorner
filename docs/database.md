# Database Structures 資料庫結構
### We use Python lists to show our database structures. This is also what you will get using the database APIs in this project.<br/><br/>我們使用 Python 串列來表示資料庫結構，此專案中的資料庫 API 亦會回傳類似的東西。
<br/>

## Games
```py
tables['Games'] = [{
    'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'name':'TEXT',
    'description': 'TEXT',
    'author_id': 'TEXT',
    'cover_image': 'BLOB',
    'entry_file': 'BLOB',  # the entry file of a game (HTML)  # 遊戲的進入點 (HTML)
    'game_files': 'BLOB',  # other game files (.js, .css, etc), not including the entry file.
                            # 其他遊戲檔案 (.js, .css 等)，不含進入點 HTML 檔。
    'highest_score': 'REAL DEFAULT 0',
    'achievement_holder': 'TEXT'
}, {
    'author_id': 'Users(uuid)',
    'achievement_holder': 'Users(uuid)'  # FK
}]
```
<br/>

## GamePlayingRecords
```py
tables['GamePlayingRecords'] = [{
    'record_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'game_id': 'INTEGER',
    'user_uuid': 'TEXT',
    'time': 'DATETIME',
    'score': 'REAL'
}, {
    'game_id': 'Games(id)',  # FK1
    'user_uuid': 'Users(uuid)'  # FK2
}]
```
