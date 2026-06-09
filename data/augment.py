import json
import re


def load_brawler_classes() -> dict[int, str]:
    with open("data/brawler_classes.json", "r") as f:
        raw = re.sub(r"//.*", "", f.read())
    return {int(k): v for k, v in json.loads(raw).items()}


def brawler_class(brawler_id: int, classes: dict[int, str]) -> str:
    if not brawler_id:
        return "none"
    return classes[brawler_id]


def pick_classes(picks: list[int], classes: dict[int, str]) -> list[str]:
    return [brawler_class(p, classes) for p in picks]


def id_to_name(battles: list) -> dict[int, str]:
    mapping = {}
    for battle in battles:
        for team in battle["teams"]:
            for player in team:
                brawler = player["brawler"]
                mapping[brawler["id"]] = brawler["name"]
    return mapping


def make_row(map_name, mode, your_picks, enemy_picks, next_pick, label, classes):
    return {
        "map": map_name,
        "mode": mode,
        "your_picks": your_picks,
        "your_pick_classes": pick_classes(your_picks, classes),
        "enemy_picks": enemy_picks,
        "enemy_pick_classes": pick_classes(enemy_picks, classes),
        "next_pick": next_pick,
        "next_pick_class": brawler_class(next_pick, classes) if next_pick else "none",
        "label": label,
    }


if __name__ == "__main__":
    with open("data/battles.json", "r") as f:
        battles = json.load(f)

    classes = load_brawler_classes()
    training_data = []

    for battle in battles:

        team0 = battle["teams"][0]
        team1 = battle["teams"][1]
        if len(team0) != 3 or len(team1) != 3:
            continue

        t0 = [p["brawler"]["id"] for p in team0]
        t1 = [p["brawler"]["id"] for p in team1]
        m, mode, label = battle["map"], battle["mode"], battle["result"]

        training_data.append(make_row(m, mode, [t0[0]], [], t1[0], label, classes))
        training_data.append(make_row(m, mode, [t0[0]], [t1[0]], t1[1], label, classes))
        training_data.append(make_row(m, mode, [t0[0]], [t1[0], t1[1]], t0[1], label, classes))
        training_data.append(make_row(m, mode, [t0[0], t0[1]], [t1[0], t1[1]], t0[2], label, classes))
        training_data.append(make_row(m, mode, t0, [t1[0], t1[1]], t1[2], label, classes))
        training_data.append(make_row(m, mode, t0, t1, [], label, classes))

    with open("data/training_data.json", "w") as f:
        json.dump(training_data, f)
    print(f"saved {len(training_data)} training rows")

    names = id_to_name(battles)
    with open("data/id_to_name.json", "w") as f:
        json.dump({str(k): v for k, v in names.items()}, f)
    print(f"saved {len(names)} brawler names")
