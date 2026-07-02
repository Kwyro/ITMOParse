import requests

URL = "https://abitlk.itmo.ru/api/v1/rating/directions?degree=bachelor"

responce = requests.get(url=URL).json()

# Получим список всех программ по коду
result = responce["result"] 
items = result["items"]    

programs = dict() # Хэш-таблица, где будут храниться все коды программ с их ID

for item in items:
    code = item['direction_title'][0:8]
    id = item['competitive_group_id']

    programs[code] = id