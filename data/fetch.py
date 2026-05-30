from itertools import count
import time
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
BRAWL_API_KEY = os.getenv("BRAWL_API_KEY")
def fetch_data():
    url = "https://api.brawlstars.com/v1/rankings/global/players?limit=200"
    headers = {
        "Authorization": f"Bearer {BRAWL_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

data = fetch_data()

tag=[player["tag"] for player in data["items"]]




def fetch_player_battles(tag):
    tag = tag.replace("#", "%23")
    url = f"https://api.brawlstars.com/v1/players/{tag}/battlelog"
    headers = {
        "Authorization": f"Bearer {BRAWL_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

#count = 0 
battles_data = []
for tag in tag:
    battles = fetch_player_battles(tag)
    for battle in battles["items"]:
        if battle["battle"]["type"] == "ranked" and (battle["battle"]["mode"] in ["gemGrab", "brawlBall", "knockout", "hotZone"]):
            battles_data.append({ 
                "mode": battle["battle"]["mode"],
                "map": battle["event"]["map"],
                "result": battle["battle"]["result"],
                "teams": battle["battle"]["teams"]
            })
            time.sleep(0.5)

with open("data/battles.json", "w") as f: 
    json.dump(battles_data, f)

try:
    data = fetch_data()
    print("fetched rankings:", len(data["items"]))
except Exception as e:
    print("error:", e)
print("script started")