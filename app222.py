from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model and label encoder
model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")

# Get list of valid locations
import pandas as pd
df = pd.read_csv("Sub_Division_IMD_2017.csv")
locations = sorted(df['SUBDIVISION'].unique())

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        location = request.form.get("location")
        try:
            rainfall = [float(request.form.get(f"year{i}")) for i in range(1, 6)]
            if location not in locations:
                error = "Invalid location selected."
            else:
                loc_code = encoder.transform([location])[0]
                features = np.array([loc_code] + rainfall).reshape(1, -1)
                prediction = model.predict(features)[0]
        except Exception as e:
            error = f"Invalid input: {e}"

    return render_template("index.html", locations=locations, prediction=prediction, error=error)

if __name__ == "__main__":
    app.run(debug=True)
