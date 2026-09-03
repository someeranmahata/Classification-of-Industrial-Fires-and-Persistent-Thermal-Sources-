# 🔥 Industrial Fire & Persistent Thermal Source Detection

A Machine Learning and Geospatial Analytics project that classifies NASA FIRMS satellite hotspots into **Industrial Fire**, **Persistent Thermal Source**, and **Other** categories. The system uses an XGBoost model for prediction and visualizes results on an interactive web dashboard.

---

## 🚀 Features

- Fetches live hotspot data from NASA FIRMS API.
- Classifies hotspots into:
  - Industrial Fire
  - Persistent Thermal Source
  - Other
- Interactive map visualization using Leaflet.js.
- Real-time hotspot statistics dashboard.
- Geospatial analysis using proximity to industrial locations.
- Historical hotspot persistence analysis.

---

## 🛠️ Tech Stack

### Machine Learning
- Python
- XGBoost
- Scikit-Learn
- Pandas
- NumPy

### Backend
- Flask
- Requests

### Geospatial Processing
- BallTree
- Haversine Distance

### Frontend
- HTML
- CSS
- JavaScript
- Leaflet.js

### Data Source
- NASA FIRMS API

---

## 📊 Workflow

1. Fetch live hotspot data from NASA FIRMS.
2. Perform preprocessing and feature engineering.
3. Generate thermal, temporal, and geospatial features.
4. Predict hotspot category using XGBoost.
5. Visualize classified hotspots on an interactive map.
6. Display real-time hotspot statistics.

---

## 🧠 Model Features

The model uses:

- Brightness Temperature
- Brightness T31
- Fire Radiative Power (FRP)
- Temperature Difference
- Distance to Nearest Industry
- Industry Proximity Indicator
- Hotspot Persistence
- Detection Count
- Month
- Scan & Track Values
- Confidence Score

---

## 🎯 Classification Classes

| Label | Category |
|---------|-----------|
| 0 | Industrial Fire |
| 1 | Persistent Thermal Source |
| 2 | Other |

---

## ⚙️ Installation

```bash

cd Industrial-Fire-Detection

pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

### Legend

🔴 Industrial Fire

🟢 Persistent Thermal Source

🟠 Other

---
