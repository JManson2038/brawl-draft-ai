import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

with open("data/training_data.json", "r") as f:
        training_data = json.load(f)

def flatten_row(row:dict):
    your_picks = row["your_picks"] + [0] * (3 - len(row["your_picks"]))
    enemy_picks = row["enemy_picks"] + [0] * (3 - len(row["enemy_picks"]))
    your_classes = row["your_pick_classes"] + ["none"] * (3 - len(row["your_pick_classes"]))
    enemy_classes = row["enemy_pick_classes"] + ["none"] * (3 - len(row["enemy_pick_classes"]))
    return {
    "your_pick_1": your_picks[0],
    "your_pick_2": your_picks[1],
    "your_pick_3": your_picks[2],
    "your_pick_1_class": your_classes[0],
    "your_pick_2_class": your_classes[1],
    "your_pick_3_class": your_classes[2],
    "enemy_pick_1": enemy_picks[0],
    "enemy_pick_2": enemy_picks[1],
    "enemy_pick_3": enemy_picks[2],
    "enemy_pick_1_class": enemy_classes[0],
    "enemy_pick_2_class": enemy_classes[1],
    "enemy_pick_3_class": enemy_classes[2],
    "next_pick": row["next_pick"] if row["next_pick"] else 0,
    "next_pick_class": row.get("next_pick_class", "none"),
    "map": row["map"],
    "mode": row["mode"],
    "label": 1 if row["label"] == "victory" else 0
}

rows = [flatten_row(row) for row in training_data]
df = pd.DataFrame(rows)
le_map = LabelEncoder()
le_mode = LabelEncoder()

df["map"] = le_map.fit_transform(df["map"])
df["mode"] = le_mode.fit_transform(df["mode"])

class_cols = [c for c in df.columns if c.endswith("_class")]
le_class = LabelEncoder()
le_class.fit(pd.unique(df[class_cols].values.ravel()))
df[class_cols] = df[class_cols].apply(lambda col: le_class.transform(col))

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(scale_pos_weight=0.5)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("accuracy:", accuracy_score(y_test, preds))

rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

rf_preds = rf_model.predict(X_test)


with open("model/xgb_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("model saved")

with open("model/le_map.pkl", "wb") as f:
    pickle.dump(le_map, f)

with open("model/le_mode.pkl", "wb") as f:
    pickle.dump(le_mode, f)

with open("model/le_class.pkl", "wb") as f:
    pickle.dump(le_class, f)

print("encoders saved")

if __name__== "__main__":
    with open("data/training_data.json", "r") as f:
        training_data = json.load(f)


print(classification_report(y_test, preds))

print(y.value_counts(normalize=True))
print(le_map.classes_)