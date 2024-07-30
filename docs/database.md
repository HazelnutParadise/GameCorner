# Database Structures 資料庫結構
### We use Python lists to show our database structures. This is also what you will get using the database APIs in this project.<br/><br/>我們使用 Python 串列來表示資料庫結構，此專案中的資料庫 API 亦會回傳類似的東西。
<br/>

## Games
```py
tables['Games'] = [{
    'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT'
    'name':'TEXT',
    'description': 'TEXT',
    'cover_image': 'BLOB',
    'entry_file': 'BLOB',
    'game_files': 'BLOB',
    'highest_score': 'REAL DEFAULT 0',
    'achievement_holder': 'TEXT'
}, {
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
    'game_name': 'Games(id)',
    'user_uuid': 'Users(uuid)'
}]
```
