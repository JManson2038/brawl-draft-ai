from fastapi import FastAPI
from pydantic import BaseModel
import json
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder

class DraftState(BaseModel):
    map: str
    mode: str
    your_picks: list
    enemy_picks: list
    your_bans: list
    enemy_bans: list

app = FastAPI()

@app.post("/recommend")
async def recommend(item: DraftState):
    return item

with open("model/xgb_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/le_map.pkl", "rb") as f:
    le_map = pickle.load(f)

with open("model/le_mode.pkl", "rb") as f:
    le_mode = pickle.load(f)

with open("data/brawlers.json", "r") as f:
    all_brawlers = json.load(f)

with open("data/id_to_name.json", "r") as f:
    id_to_name = json.load(f)