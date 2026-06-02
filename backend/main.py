from fastapi import  FastAPI
from pydantic import BaseModel
import json
import pickle
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
from data.augment import id_to_name

class Draftstate(BaseModel):
    map:str
    mode: str 
    your_picks: list
    enemy_picks: list
    your_bans: list
    enemy_bans: list
# Create the main API application instance
app = FastAPI()

# Define a root path operation
@app.post("/recommend")
async def create_item(item: Draftstate ):
    return item

with open("data/training_data.json", "r") as f:
    data = json.load(f)

brawlers = set()
for row in data:
    for p in row["your_picks"] + row["enemy_picks"]:
        if p != 0:
            brawlers.add(p)
    if row["next_pick"]:
        brawlers.add(row["next_pick"])

brawlers = list(brawlers)

with open("data/brawlers.json", "w") as f:
    json.dump(brawlers, f)

print("saved", len(brawlers), "brawlers")
with open("data/battles.json", "r") as f:
    battles = json.load(f)
names = id_to_name(battles)
with open("data/id_to_name.json", "w") as f:
    json.dump({str(k): v for k, v in names.items()}, f)

print("saved", len(names), "brawler names")