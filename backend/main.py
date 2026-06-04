from fastapi import FastAPI
from pydantic import BaseModel
import json
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd

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
    used = item.your_picks + item.enemy_picks + item.your_bans + item.enemy_bans
    available = [b for b in all_brawlers if b not in used]

    picks = []
    for b in available:
        your_picks = item.your_picks + [0] * (3 - len(item.your_picks))
        enemy_picks = item.enemy_picks + [0] * (3 - len(item.enemy_picks))
        row = [
            your_picks[0], your_picks[1], your_picks[2],
            enemy_picks[0], enemy_picks[1], enemy_picks[2],
            b,
            le_map.transform([item.map])[0],
            le_mode.transform([item.mode])[0]
        ]
        picks.append(row)
    
    X = pd.DataFrame(picks, columns=["your_pick_1","your_pick_2","your_pick_3","enemy_pick_1","enemy_pick_2","enemy_pick_3","next_pick","map","mode"])
    probs = model.predict_proba(X)[:, 1]
    top5_idx = np.argsort(probs)[::-1][:5]
    results = [{"brawler": id_to_name[str(available[i])], "win_prob": float(probs[i])} for i in top5_idx]
    return {"recommendations": results}
    

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