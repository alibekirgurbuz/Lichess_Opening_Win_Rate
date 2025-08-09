# model.py

import requests
import json
from typing import List, Dict, Tuple, Optional


def get_games_from_lichess(username: str, max_games: int) -> Tuple[Optional[List[Dict]], Optional[str]]:
    """
    Belirtilen kullanıcı için Lichess API'den oyunları alır.
    """
    url = f"https://lichess.org/api/games/user/{username}"
    headers = {"Accept": "application/x-ndjson"}
    params = {"max": max_games, "opening": "true"}

    try:
        response = requests.get(url, headers=headers, params=params, stream=True)
        response.raise_for_status()  # HTTP hataları için istisna fırlatır

        games = []
        for line in response.iter_lines():
            if line:
                try:
                    games.append(json.loads(line.decode('utf-8')))
                except json.JSONDecodeError:
                    continue
        return games, None
    except requests.exceptions.RequestException as e:
        return None, f"API bağlantı hatası: {str(e)}"
    except Exception as e:
        return None, f"Beklenmedik bir hata oluştu: {str(e)}"