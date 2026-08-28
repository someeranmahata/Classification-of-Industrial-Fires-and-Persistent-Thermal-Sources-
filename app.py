from flask import Flask, render_template, jsonify, request
import pickle
import pandas as pd
import numpy as np
import requests
from sklearn.neighbors import BallTree
from xgboost import XGBClassifier
import os



app = Flask(__name__)

API_KEY = "4022da14d11859bbc865df890e2ab6af"

# ------------------------
# Load model
# ------------------------

model = XGBClassifier()
model.load_model('industrial_fire_model.json')

with open("history_lookup.pkl", "rb") as f:
    history_dict = pickle.load(f)

industry_df = pd.read_csv("industry_locations.csv")

industry_tree = BallTree(
    np.radians(
        industry_df[["latitude", "longitude"]]
    ),
    metric="haversine"
)

# ------------------------
# Feature generation
# ------------------------

def generate_features(row):

    lat = row["latitude"]
    lon = row["longitude"]

    temp_diff = (
        row["brightness"]
        - row["bright_t31"]
    )

    point = np.radians([[lat, lon]])

    dist, _ = industry_tree.query(
        point,
        k=1
    )

    distance_to_industry = (
        dist[0][0] * 6371
    )

    industry_nearby = int(
        distance_to_industry <= 5
    )

    persistence, detection_count = (
        history_dict.get(
            (
                round(lat, 2),
                round(lon, 2)
            ),
            (1, 1)
        )
    )

    confidence_map = {
        "l": 0,
        "n": 1,
        "h": 2
    }

    confidence_num = confidence_map.get(
        str(row["confidence"]).lower(),
        1
    )

    month = pd.to_datetime(
        row["acq_date"]
    ).month

    return pd.DataFrame([{
        "brightness": row["brightness"],
        "bright_t31": row["bright_t31"],
        "frp": row["frp"],
        "temp_diff": temp_diff,
        "distance_to_industry": distance_to_industry,
        "industry_nearby": industry_nearby,
        "persistence": persistence,
        "detection_count": detection_count,
        "month": month,
        "scan": row["scan"],
        "track": row["track"],
        "confidence_num": confidence_num
    }])

# ------------------------
# Fetch FIRMS
# ------------------------

def fetch_firms(days):

    url = (
    f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    f"{API_KEY}/"
    f"VIIRS_NOAA21_NRT/"
    f"68,6,98,38/"
    f"{days}"
)

    df = pd.read_csv(url)
    
    df["brightness"] = df["bright_ti4"]
    df["bright_t31"] = df["bright_ti5"]
    
    
    return df


# ------------------------
# TESTING PURPOSE
# ------------------------
'''
results2=[]
for i in range(5):
    row = fire.iloc[i]
    # print(row, type(row))
    X = generate_features(
        row.to_dict()
       )

    pred = model.predict(X)[0]
    print(row['longitude'], row['latitude'],pred)
    results2.append({
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "prediction": int(pred),
            "brightness": row["brightness"],
            "frp": row["frp"]
        })
    # print(results2)

'''




    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/hotspots")
def hotspots():

    days = int(
        request.args.get("days", 1)
    )

    firms_df = fetch_firms(days)

    results = []
    print("hotspot coord: ",firms_df.shape[0])

    for _, row in firms_df.iterrows():

        X = generate_features(
            row.to_dict()
        )

        pred = model.predict(X)[0]

        results.append({
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "prediction": int(pred),
            "brightness": row["brightness"],
            "frp": row["frp"]
        })
    
    # print(results)
    
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
    

