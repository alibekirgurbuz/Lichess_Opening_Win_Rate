# analyzer.py

from typing import List, Dict, Tuple, Optional


def analyze_openings(games: List[Dict], username: str, color_filter: str, limit: int) -> Tuple[
    List[Tuple], Optional[str]]:
    """
    Verilen oyun listesini analiz ederek en çok oynanan açılışları bulur.
    """
    acilislar = {}

    for game in games:
        if "opening" in game and "players" in game and "status" in game:
            acilis_adi = game["opening"]["name"]

            white_player = game["players"]["white"].get("user", {}).get("name", "").lower()
            black_player = game["players"]["black"].get("user", {}).get("name", "").lower()

            is_white = white_player == username.lower()
            is_black = black_player == username.lower()

            if (color_filter == "white" and not is_white) or \
                    (color_filter == "black" and not is_black):
                continue

            color_info = "Beyaz" if is_white else "Siyah"
            full_opening_name = f"{acilis_adi} ({color_info})"

            if full_opening_name not in acilislar:
                acilislar[full_opening_name] = {"total": 0, "wins": 0}

            acilislar[full_opening_name]["total"] += 1

            if "winner" in game:
                user_won = (game["winner"] == "white" and is_white) or \
                           (game["winner"] == "black" and is_black)
                if user_won:
                    acilislar[full_opening_name]["wins"] += 1

    acilis_listesi = []
    for acilis, stats in acilislar.items():
        total = stats["total"]
        wins = stats["wins"]
        win_rate = (wins / total * 100) if total > 0 else 0
        acilis_listesi.append((acilis, total, win_rate))

    en_cok_oynananlar = sorted(acilis_listesi, key=lambda x: x[1], reverse=True)[:limit]

    return en_cok_oynananlar, None