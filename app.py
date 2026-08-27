from flask import Flask, render_template
import pickle
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from xgboost import XGBClassifier

# persistence lookup
with open("history_lookup.pkl", "rb") as f:
    history_dict = pickle.load(f)

with open("industrial_fire_model.pkl", "rb") as f:
    model_testing = pickle.load(f)

# industries
industry_df = pd.read_csv("industry_locations.csv")

industry_tree = BallTree(
    np.radians(industry_df[["latitude", "longitude"]]),
    metric="haversine"
)

def generate_features(firms_data):

    lat = firms_data["latitude"]
    lon = firms_data["longitude"]

    # ----------------------------------
    # temp_diff
    # ----------------------------------
    temp_diff = (
        firms_data["brightness"]
        - firms_data["bright_t31"]
    )

    # ----------------------------------
    # nearest industry
    # ----------------------------------
    point = np.radians([[lat, lon]])

    dist, idx = industry_tree.query(
        point,
        k=1
    )

    distance_to_industry = (
        dist[0][0] * 6371
    )

    industry_nearby = int(
        distance_to_industry <= 5
    )

    # ----------------------------------
    # persistence + detection count
    # ----------------------------------
    persistence, detection_count = (
        history_dict.get(
            (
                round(lat, 2),
                round(lon, 2)
            ),
            (1, 1)
        )
    )

    # ----------------------------------
    # month
    # ----------------------------------
    month = pd.to_datetime(
        firms_data["acq_date"]
    ).month

    # ----------------------------------
    # confidence
    # ----------------------------------
    confidence_map = {
        "l": 0,
        "n": 1,
        "h": 2
    }

    confidence_num = confidence_map.get(
        str(
            firms_data["confidence"]
        ).lower(),
        1
    )

    # ----------------------------------
    # model dataframe
    # ----------------------------------
    X = pd.DataFrame([{
        "brightness":
            firms_data["brightness"],

        "bright_t31":
            firms_data["bright_t31"],

        "frp":
            firms_data["frp"],

        "temp_diff":
            temp_diff,

        "distance_to_industry":
            distance_to_industry,

        "industry_nearby":
            industry_nearby,

        "persistence":
            persistence,

        "detection_count":
            detection_count,

        "month":
            month,

        "scan":
            firms_data["scan"],

        "track":
            firms_data["track"],

        "confidence_num":
            confidence_num
    }])

    return X
#random data from dataset for testing
firms_data = pd.DataFrame([{
    "latitude": 25.32909,
    "longitude": 94.71902,
    "brightness": 330.71,
    "scan": 0.62,
    "track": 0.71,
    "acq_date": "2021-01-01",
    "acq_time": 554,
    "satellite": "SNPP",
    "instrument": "SNPP",
    "confidence": "n",
    "version": 2,
    "bright_t31": 289.06,
    "frp": 6.72,
    "daynight": "D",
    "type": 0
}])

print(firms_data.head())
x = generate_features(firms_data.iloc[0].to_dict())
model_testing.predict(x)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)