# Brawl Draft AI

A Brawl Stars ranked draft simulator that uses machine learning to recommend the best brawler picks based on the current draft state, map, and mode.

## What it does

- Scrapes ranked battle data from the official Brawl Stars API across 11 countries
- Trains an XGBoost model on ~107k augmented draft states from Masters+ players
- Serves brawler recommendations via a FastAPI backend
- Provides a dark-themed frontend where you can set bans, picks, and get real-time recommendations

**Model accuracy: ~71.6%** on ranked 3v3 battle outcomes (Brawl Ball, Gem Grab, Knockout, Hot Zone)

## Tech stack

- **Data**: Brawl Stars official API, Python
- **Model**: XGBoost with brawler class features and snake draft augmentation
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS with Brawlify CDN portraits

## Project structure

```
brawl-draft-ai/
├── data/
│   ├── fetch.py          # scrapes battle data from API
│   ├── augment.py        # builds training rows via snake draft simulation
│   ├── win_rates.py      # calculates per-brawler win rates per map
│   ├── dedup.py          # deduplicates battle data
│   ├── battles.json      # raw battle data
│   ├── training_data.json
│   ├── brawler_classes.json
│   └── id_to_name.json
├── model/
│   ├── train.py          # trains XGBoost model
│   ├── xgb_model.pkl
│   ├── le_map.pkl
│   ├── le_mode.pkl
│   └── le_class.pkl
├── backend/
│   └── main.py           # FastAPI recommendation endpoint
├── frontend/
│   └── index.html        # draft simulator UI
└── .env                  # BRAWL_API_KEY
```

## Setup

### 1. Install dependencies

```bash
pip install fastapi uvicorn xgboost scikit-learn pandas python-dotenv requests
```

### 2. Set up your API key

Create a `.env` file:

```
BRAWL_API_KEY=your_key_here
```

Get a key at [developer.brawlstars.com](https://developer.brawlstars.com). Whitelist your IP.

### 3. Fetch data and train the model

```bash
python data/fetch.py
python data/augment.py
python model/train.py
```

### 4. Run the backend

```bash
uvicorn backend.main:app --reload
```

### 5. Run the frontend

```bash
python -m http.server 3000 --directory frontend
```

Open `http://localhost:3000` in your browser.

## API

**POST /recommend**

```json
{
  "map": "Sneaky Fields",
  "mode": "brawlBall",
  "your_picks": [16000039],
  "enemy_picks": [16000011],
  "your_bans": [16000104],
  "enemy_bans": []
}
```

Returns top 5 brawler recommendations with win probabilities.