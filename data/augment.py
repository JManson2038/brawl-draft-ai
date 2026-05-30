import json

with open("data/battles.json", "r") as f:
    battles = json.load(f)

training_data = []
for battle in battles:

    team0 = battle["teams"][0]
    team1 = battle["teams"][1]

    row1 = {
        "map":battle["map"],
        "mode": battle["mode"],
        "your_picks": [team0[0]["brawler"]["name"]],
        "enemy_picks": [],
        "next_pick": team1[0]["brawler"]["name"],
        "label": battle["result"]
    }
    training_data.append(row1)

    row2 = {
        "map":battle["map"],
        "mode": battle["mode"],
        "your_picks": [team0[0]["brawler"]["name"]],
        "enemy_picks": [team1[0]["brawler"]["name"]],
        "next_pick": team1[1]["brawler"]["name"],
        "label": battle["result"]
    }
    training_data.append(row2)

    row3 = {
        "map":battle["map"],
        "mode": battle["mode"],
        "your_picks": [team0[0]["brawler"]["name"]],
        "enemy_picks": [team1[0]["brawler"]["name"], team1[1]["brawler"]["name"]],
        "next_pick": team0[1]["brawler"]["name"],
        "label": battle["result"]
    }
    training_data.append(row3)

    row4 = {
        "map":battle["map"],
        "mode": battle["mode"],
        "your_picks": [team0[0]["brawler"]["name"],team0[1]["brawler"]["name"]],
        "enemy_picks": [team1[0]["brawler"]["name"], team1[1]["brawler"]["name"]],
        "next_pick": team0[2]["brawler"]["name"] ,
        "label": battle["result"]
    }
    training_data.append(row4)

    row5 = {
        "map":battle["map"],
        "mode": battle["mode"],
        "your_picks": [team0[0]["brawler"]["name"],team0[1]["brawler"]["name"],team0[2]["brawler"]["name"]],
        "enemy_picks": [team1[0]["brawler"]["name"], team1[1]["brawler"]["name"]],
        "next_pick": team1[2]["brawler"]["name"] ,
        "label": battle["result"]
    }
    training_data.append(row5)

    row6 = {
        "map":battle["map"],
        "mode": battle["mode"],
        "your_picks": [team0[0]["brawler"]["name"],team0[1]["brawler"]["name"],team0[2]["brawler"]["name"]],
        "enemy_picks": [team1[0]["brawler"]["name"], team1[1]["brawler"]["name"], team1[2]["brawler"]["name"]],
        "next_pick":[],
        "label": battle["result"]
    }
    training_data.append(row6)

with open("training_data.json", "w") as f: 
    json.dump(training_data, f)
print(f"saved {len(training_data)} training rows")





