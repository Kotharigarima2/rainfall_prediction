from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import json
import requests

app = Flask(__name__)

# —————————————————————————————————————————————————————————————
# 1) Load Models & Encoders
# —————————————————————————————————————————————————————————————
monthly_model    = joblib.load("rf_model_annual.pkl")
monthly_encoder  = joblib.load("monthly_encoder.pkl")
annual_model     = joblib.load("model.pkl")
annual_encoder   = joblib.load("encoder.pkl")

# —————————————————————————————————————————————————————————————
# 2) Load Subdivision List (for dropdowns)
# —————————————————————————————————————————————————————————————
df_monthly        = pd.read_csv("Sub_Division_IMD_2017.csv")
monthly_locations = sorted(df_monthly['SUBDIVISION'].unique())
annual_locations  = monthly_locations.copy()

# —————————————————————————————————————————————————————————————
# 3) Subdivision metadata (info + coordinates)
#    Used by both backend (/weather) and frontend (subdivisionInfo)
# —————————————————————————————————————————————————————————————
subdivisions = {
     "Andaman & Nicobar Islands": {"info": "Island tropics", "lat": 11.7, "lon": 92.7},
    "Arunachal Pradesh": {"info": "Himalayan foothills", "lat": 28.2, "lon": 94.0},
    "Assam & Meghalaya": {"info": "Valleys & hills", "lat": 26.2, "lon": 91.7},
    "Bihar": {"info": "Gangetic plains", "lat": 25.6, "lon": 85.1},
    "Chhattisgarh": {"info": "Central Indian plains", "lat": 21.3, "lon": 81.6},
    "Coastal Andhra Pradesh": {"info": "Coastal strip", "lat": 16.5, "lon": 81.3},
    "Coastal Karnataka": {"info": "Konkan coast", "lat": 13.3, "lon": 74.7},
    "East Madhya Pradesh": {"info": "Vindhyan uplands", "lat": 23.5, "lon": 80.0},
    "East Rajasthan": {"info": "Arid desert & plains", "lat": 26.0, "lon": 75.0},
    "East Uttar Pradesh": {"info": "Tropical plains", "lat": 26.8, "lon": 83.0},
    "Gangetic West Bengal": {"info": "Delta plains", "lat": 23.0, "lon": 87.9},
    "Gujarat Region": {"info": "Western plains", "lat": 22.3, "lon": 72.6},
    "Haryana Delhi & Chandigarh": {"info": "Indo-Gangetic plain", "lat": 28.6, "lon": 77.2},
    "Himachal Pradesh": {"info": "Himalayan mid-hills", "lat": 31.1, "lon": 77.2},
    "Jammu & Kashmir": {"info": "High Himalayas", "lat": 34.1, "lon": 74.8},
    "Jharkhand": {"info": "Chota Nagpur plateau", "lat": 23.6, "lon": 85.3},
    "Kerala": {"info": "Tropical coast & hills", "lat": 10.5, "lon": 76.2},
    "Konkan & Goa": {"info": "Coastal region", "lat": 16.7, "lon": 73.8},
    "Lakshadweep": {"info": "Coral atolls", "lat": 10.6, "lon": 72.6},
    "Madhya Maharashtra": {"info": "Deccan plateau", "lat": 19.0, "lon": 74.0},
    "Matathwada": {"info": "Semi-arid plateau", "lat": 19.3, "lon": 76.2},
    "Naga Mani Mizo Tripura": {"info": "NE hill states (NM, MZ, TR)", "lat": 25.6, "lon": 93.9},
    "North Interior Karnataka": {"info": "Semi-arid plateau", "lat": 15.3, "lon": 75.7},
    "Orissa": {"info": "Coastal & plateaus mix", "lat": 20.3, "lon": 85.8},
    "Punjab": {"info": "Wheat belt plains", "lat": 31.1, "lon": 75.4},
    "Rayalseema": {"info": "Semi-arid interior", "lat": 14.7, "lon": 78.2},
    "Saurashtra & Kutch": {"info": "Dry arid region", "lat": 22.2, "lon": 70.3},
    "South Interior Karnataka": {"info": "Coastal plateau", "lat": 12.3, "lon": 76.6},
    "Sub Himalayan West Bengal & Sikkim": {"info": "Terai foothills", "lat": 26.7, "lon": 88.4},
    "Tamil Nadu": {"info": "Coastal & plains", "lat": 11.1, "lon": 78.6},
    "Telangana": {"info": "Deccan plateau", "lat": 17.4, "lon": 78.5},
    "Uttarakhand": {"info": "Shivalik foothills", "lat": 30.0, "lon": 79.0},
    "Vidarbha": {"info": "Mahanadi basin", "lat": 20.7, "lon": 78.9},
    "West Madhya Pradesh": {"info": "Malwa plateau", "lat": 22.7, "lon": 75.9},
    "West Rajasthan": {"info": "Thar desert region", "lat": 26.9, "lon": 70.9},
    "West Uttar Pradesh": {"info": "Granary region", "lat": 28.6, "lon": 77.2}
}

# Ha
# 4) API Key
WEATHER_API_KEY = "a4b4f753d0ec9116b71567048f03a92a"

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence_interval = None
    error = None
    prediction_type = None
    input_data = {}

    if request.method == "POST":
        prediction_type = request.form.get("prediction_type")

        if prediction_type == "monthly":
            try:
                loc = request.form["monthly_subdivision"]
                may, jun, jul, aug, sep = [float(request.form[m]) for m in ("may","jun","jul","aug","sep")]
                input_data = dict(may=may, jun=jun, jul=jul, aug=aug, sep=sep)
                loc_code = monthly_encoder.transform([loc])[0]
                feats = np.array([[loc_code, may, jun, jul, aug, sep]])

                preds = [est.predict(feats)[0] for est in monthly_model.estimators_]
                mean_p = np.mean(preds); std_p = np.std(preds)
                prediction = mean_p
                confidence_interval = (
                    round(mean_p - 1.96*std_p, 2),
                    round(mean_p + 1.96*std_p, 2)
                )
            except Exception as e:
                error = f"Monthly error: {e}"

        elif prediction_type == "annual":
            try:
                loc   = request.form["annual_location"]
                rains = [float(request.form[f"year{i}"]) for i in range(1,6)]
                loc_code = annual_encoder.transform([loc])[0]
                feats    = np.array([loc_code] + rains).reshape(1, -1)

                # confidence interval over the RF estimators
                preds = [est.predict(feats)[0] for est in annual_model.estimators_]
                mean_p = np.mean(preds); std_p = np.std(preds)
                prediction = mean_p
                confidence_interval = (
                    round(mean_p - 1.96*std_p, 2),
                    round(mean_p + 1.96*std_p, 2)
                )
            except Exception as e:
                error = f"Annual error: {e}"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence_interval=confidence_interval,
        prediction_type=prediction_type,
        error=error,
        input_data=input_data,
        monthly_locations=monthly_locations,
        annual_locations=annual_locations,
        subdivision_info=json.dumps({k: v["info"] for k, v in subdivisions.items()})
    )

@app.route("/weather")
def weather():
    sub = request.args.get("subdivision")
    meta = subdivisions.get(sub)
    if not meta:
        return jsonify(error="Unknown subdivision"), 400

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={meta['lat']}&lon={meta['lon']}"
        f"&appid={WEATHER_API_KEY}&units=metric"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify(error="Weather service error"), 502

    d = resp.json()
    return jsonify(
        temp=d["main"]["temp"],
        humidity=d["main"]["humidity"],
        description=d["weather"][0]["description"]
    )

if __name__ == "__main__":
    app.run(debug=True)