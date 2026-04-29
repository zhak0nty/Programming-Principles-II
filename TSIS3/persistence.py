import json
from pathlib import Path


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal",
}

DIFFICULTIES = {"easy", "normal", "hard"}
CAR_COLORS = {"blue", "green", "orange"}


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return fallback


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_settings(path: Path):
    data = load_json(path, DEFAULT_SETTINGS.copy())
    merged = DEFAULT_SETTINGS.copy()
    if isinstance(data, dict):
        merged.update(data)
    if merged["difficulty"] not in DIFFICULTIES:
        merged["difficulty"] = "normal"
    if merged["car_color"] not in CAR_COLORS:
        merged["car_color"] = "blue"
    merged["sound"] = bool(merged.get("sound", True))
    return merged


def save_settings(path: Path, settings) -> None:
    save_json(path, settings)


def load_leaderboard(path: Path):
    board = load_json(path, [])
    if not isinstance(board, list):
        return []
    clean = []
    for item in board:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "Player"))[:18]
        score = int(item.get("score", 0))
        distance = int(item.get("distance", 0))
        clean.append({"name": name, "score": score, "distance": distance})
    clean.sort(key=lambda x: x["score"], reverse=True)
    return clean[:10]


def add_leaderboard_entry(path: Path, name: str, score: int, distance: int):
    board = load_leaderboard(path)
    board.append(
        {
            "name": (name or "Player")[:18],
            "score": int(score),
            "distance": int(distance),
        }
    )
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]
    save_json(path, board)
    return board
