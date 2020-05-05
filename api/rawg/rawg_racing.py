"""
Francesco Giraudo
Classe 5A ROB
Codice per fare richiesta dei giochi più popolari degli ultimi 20 anni,
andando a salvare il più aggiunto anno per anno.
"""

import requests
import sqlite3 as sqlite

URL = 'https://api.rawg.io/api/games'

# ?genres=racing&ordering=-rating,-rating_count&page_size=1&dates=*1*-01-01,*2*-12-31
params = {
    'genres':'racing',
    'ordering':'-added,-rating,-rating_count',
    'page_size':1,
    'dates':''}

THIS_YEAR = 2020

dates_def = '*-01-01,*-12-31'

games_id = []

for year in range(THIS_YEAR-20, THIS_YEAR+1):
    dates = dates_def.replace(f'*', f'{year}')
    params['dates'] = dates
    
    r = requests.get(url=URL, params=params)

    game = r.json()

    games_id.append(game['results'][0]['id'])

all_games_data = []

for gid in games_id:
    r = requests.get(url=URL+f'/{gid}')

    game_data = r.json()

    all_games_data.append( (game_data['slug'], game_data['name'], game_data['released'], float(game_data['rating']) , game_data['description_raw']) )


INSERT_QUERY = "INSERT INTO 'games'(slug, name, released, rating, description_raw) VALUES (?, ?, ?, ?, ?)"

conn = sqlite.connect('db.db')
cursor = conn.cursor()

cursor.executemany(INSERT_QUERY, all_games_data)
conn.commit()

cursor.close()
conn.close()