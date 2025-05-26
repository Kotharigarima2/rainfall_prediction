🌧️ Rainfall Prediction Web App
A machine learning-powered web application that predicts rainfall for Indian subdivisions based on user input. The application also integrates live weather data, interactive charts, and user-friendly features such as dark mode and a clean interface.

📌 Features
🔮 Predicts rainfall using trained machine learning models

📈 Interactive rainfall trend charts using Chart.js

🌍 Live weather information using OpenWeatherMap API

🌗 Dark Mode toggle for better UX

📊 Model confidence score display

🗺️ Subdivision information and context

🖼️ Clean UI with background image and centered content

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

ML Model: Trained using scikit-learn

Data: IMD Rainfall dataset

APIs: OpenWeatherMap for live weather

🚀 How to Run Locally
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/rainfall-prediction.git
cd rainfall-prediction
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up API Key

Replace the OpenWeatherMap API key in your app.py:

python
Copy
Edit
API_KEY = "your_api_key_here"
Run the app

bash
Copy
Edit
python app.py
Open in browser

Visit http://127.0.0.1:5000/ to access the app.

🗂️ Project Structure
php
Copy
Edit
rainfall-prediction/
│
├── app.py                    # Flask app entry point
├── requirements.txt          # Python dependencies
├── models/                   # Trained ML models and encoders
├── data/
│   └── Sub_Division_IMD_2017.csv  # Dataset used for predictions
├── templates/
│   └── index.html            # Main UI template
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── chart.js         # Chart.js integration
📊 Model Information
Algorithm used: [e.g., Random Forest / Linear Regression / XGBoost]

Features: Subdivision, Month, Year, etc.

Trained using historical rainfall data from the Indian Meteorological Department (IMD)

📷 Screenshots
Add some UI screenshots here if you have.

🙋‍♀️ Author
Garima Kothari
B.Tech CSE, Graphic Era Hill University
Cybersecurity Enthusiast | Python & ML Learner

Feel free to connect on LinkedIn or GitHub!

📄 License
This project is licensed under the MIT License.
