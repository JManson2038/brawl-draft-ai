from itertools import count
import time
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
BRAWL_API_KEY = os.getenv("BRAWL_API_KEY")
def fetch_data(country="global"):
    url = url = f"https://api.brawlstars.com/v1/rankings/{country}/players?limit=200"
    headers = {
        "Authorization": f"Bearer {BRAWL_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()



countries = ["global", "US", "BR", "DE", "FR", "KR", "TR", "RU", "ES", "PL", "MX"]
tags = set()

for country in countries:
    data = fetch_data(country)
    for player in data["items"]:
        tags.add(player["tag"])

tags = list(tags)
print(f"collected {len(tags)} unique players")


def fetch_player_battles(tag):
    tag = tag.replace("#", "%23")
    url = f"https://api.brawlstars.com/v1/players/{tag}/battlelog"
    headers = {
        "Authorization": f"Bearer {BRAWL_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

battles_data = []
for tag in tags:
    print(f"fetching battles for {tag}...")
    battles = fetch_player_battles(tag)
   
    if "items" not in battles:
        print(f"skipping {tag}: {battles}")
        continue
    for battle in battles["items"]:
        if battle["event"]["map"] is None:
            continue
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