import json
import os

def load_settings():
    defaults = {"sound": True, "car_color": [0, 255, 0], "difficulty": "normal"}
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f:
                loaded = json.load(f)
                defaults.update(loaded)
        except:
            pass
    return defaults

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=2)

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        try:
            with open("leaderboard.json", "r") as f:
                return json.load(f)
        except:
            pass
    return []

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=2)

def add_score(name, score, distance):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score, "distance": distance})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1
    save_leaderboard(leaderboard)
    return leaderboard