import requests
import time
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('API_KEY')
STEAM_ID = os.getenv('STEAM_ID')
url = os.getenv('URL')

params = {
    'key': API_KEY,
    'steamid': STEAM_ID,
    'format': 'json'
}

def get_store_data(app_id):
    store_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    retries = 3
    delay = 2

    for attempt in range(retries):
        store_response = requests.get(store_url)

        if store_response.status_code == 200:
            return store_response.json()

        print(f"Error fetching data for App ID {app_id}. Retrying... ({attempt + 1}/{retries})")
        time.sleep(delay)
        delay *= 2

    print(f"Failed to retrieve data for App ID {app_id} after {retries} attempts.")
    return None


response = requests.get(url, params=params)

data = response.json()
if 'response' in data and 'games' in data['response']:
    games = data['response']['games']
    game_list = []

    for game in games:
        app_id = game['appid']
        playtime_hours = round(game['playtime_forever'] / 60, 1)
        last_played = game.get('rtime_last_played', 0)
        last_played_date = 'N/A'

        if last_played > 0:
            last_played_date = datetime.utcfromtimestamp(last_played).strftime('%Y-%m-%d %H:%M:%S')

        store_data = get_store_data(app_id)

        if store_data and str(app_id) in store_data and store_data[str(app_id)].get('success', False):
            game_title = store_data[str(app_id)]['data'].get('name', 'N/A')
            release_date = store_data[str(app_id)]['data'].get('release_date', {}).get('date', 'N/A')
            developer = store_data[str(app_id)]['data'].get('developers', ['N/A'])[0]
            publisher = store_data[str(app_id)]['data'].get('publishers', ['N/A'])[0]

            genres = [genre['description'] for genre in
                      store_data[str(app_id)]['data'].get('genres', [{'description': 'N/A'}])]
            genres = ', '.join(genres[:2])  # Limit to the first 2 genres

            categories = store_data[str(app_id)]['data'].get('categories', [])
            mode = 'N/A'
            for category in categories:
                if category['description'] == 'Single-player':
                    mode = 'Single-player'
                    break
                elif category['description'] == 'Multiplayer':
                    mode = 'Multiplayer'
                    break
        else:
            game_title = 'N/A'
            release_date = 'N/A'
            developer = 'N/A'
            publisher = 'N/A'
            genres = 'N/A'
            mode = 'N/A'

        if sum([1 for val in [game_title, release_date, developer, publisher, genres, mode, last_played_date] if
                val == 'N/A']) < 3:
            game_info = {
                'Title': game_title,
                'Hours Played': playtime_hours,
                'App ID': app_id,
                'Release Date': release_date,
                'Developer': developer,
                'Publisher': publisher,
                'Genre': genres,
                'Mode': mode,
                'Last Play Date': last_played_date
            }
            game_list.append(game_info)

    df = pd.DataFrame(game_list)

    df = df.sort_values(by='Hours Played', ascending=False)

    df.to_csv('steam_games_sorted_by_hours_with_limited_genres.csv', index=False)
    print(df)
else:
    print("Error: Missing 'response' or 'games' in the API response.")
