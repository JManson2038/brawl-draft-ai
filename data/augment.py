import json


def id_to_name(battles: list) -> dict[int, str]:
    mapping = {}
    for battle in battles:
        for team in battle["teams"]:
            for player in team:
                brawler = player["brawler"]
                mapping[brawler["id"]] = brawler["name"]
    return mapping


if __name__ == "__main__":
    with open("data/battles.json", "r") as f:
        battles = json.load(f)

    training_data = []

    for battle in battles:

        team0 = battle["teams"][0]
        team1 = battle["teams"][1]

        row1 = {
            "map":battle["map"],
            "mode": battle["mode"],
            "your_picks": [team0[0]["brawler"]["id"]],
            "enemy_picks": [],
            "next_pick": team1[0]["brawler"]["id"],
            "label": battle["result"]
        }
        training_data.append(row1)

        row2 = {
            "map":battle["map"],
            "mode": battle["mode"],
            "your_picks": [team0[0]["brawler"]["id"]],
            "enemy_picks": [team1[0]["brawler"]["id"]],
            "next_pick": team1[1]["brawler"]["id"],
            "label": battle["result"]
        }
        training_data.append(row2)

        row3 = {
            "map":battle["map"],
            "mode": battle["mode"],
            "your_picks": [team0[0]["brawler"]["id"]],
            "enemy_picks": [team1[0]["brawler"]["id"], team1[1]["brawler"]["id"]],
            "next_pick": team0[1]["brawler"]["id"],
            "label": battle["result"]
        }
        training_data.append(row3)

        row4 = {
            "map":battle["map"],
            "mode": battle["mode"],
            "your_picks": [team0[0]["brawler"]["id"],team0[1]["brawler"]["id"]],
            "enemy_picks": [team1[0]["brawler"]["id"], team1[1]["brawler"]["id"]],
            "next_pick": team0[2]["brawler"]["id"] ,
            "label": battle["result"]
        }
        training_data.append(row4)

        row5 = {
            "map":battle["map"],
            "mode": battle["mode"],
            "your_picks": [team0[0]["brawler"]["id"],team0[1]["brawler"]["id"],team0[2]["brawler"]["id"]],
            "enemy_picks": [team1[0]["brawler"]["id"], team1[1]["brawler"]["id"]],
            "next_pick": team1[2]["brawler"]["id"] ,
            "label": battle["result"]
        }
        training_data.append(row5)

        row6 = {
            "map":battle["map"],
            "mode": battle["mode"],
            "your_picks": [team0[0]["brawler"]["id"],team0[1]["brawler"]["id"],team0[2]["brawler"]["id"]],
            "enemy_picks": [team1[0]["brawler"]["id"], team1[1]["brawler"]["id"], team1[2]["brawler"]["id"]],
            "next_pick":[],
            "label": battle["result"]
        }
        training_data.append(row6)

    with open("data/training_data.json", "w") as f:
        json.dump(training_data, f)
    print(f"saved {len(training_data)} training rows")

    names = id_to_name(battles)
    with open("data/id_to_name.json", "w") as f:
        json.dump({str(k): v for k, v in names.items()}, f)
    print(f"saved {len(names)} brawler names")
