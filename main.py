import requests
from datetime import datetime
import os

os.environ["NUTRITIONIX_APP_ID"] = "cfed2c40"
os.environ["NUTRITIONIX_API_KEY"] = "3b272f45197f0a101552b7db1fe3d5c3"
os.environ["SHEET_TOKEN"] = "Bearer Misiatysvsvsvsvsvsdvefdwefqewrtjejetbsrbrtgfqwf2"

NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
SHEET_TOKEN = os.environ.get("SHEET_TOKEN")

nutritionix_headers = {"x-app-id": NUTRITIONIX_APP_ID, "x-app-key": NUTRITIONIX_API_KEY}
sheet_headers = {
    "Content-Type": "application/json",
    "Authorization": SHEET_TOKEN,
}

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = (
    "https://api.sheety.co/3ecb86b5c571f6340fba2d7e39382dde/workout/arkusz1"
)

exercise = input("What was your exercise today?:\n>> ")


nutritionix_params = {
    "query": exercise,
    "gender": "male",
    "weight_kg": 85.4,
    "height_cm": 185.64,
    "age": 20,
}

exercise_response = requests.post(
    url=nutritionix_endpoint, json=nutritionix_params, headers=nutritionix_headers
)
exercise_response.raise_for_status()
exerciseses_json = exercise_response.json()

now = datetime.now()
todays_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")

for exercise in exerciseses_json["exercises"]:
    row_data = {
        "arkusz1": {
            "date": todays_date,
            "time": current_time,
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    post_row = requests.post(url=sheet_endpoint, json=row_data, headers=sheet_headers)
    post_row.raise_for_status()
    print("Added to spreadsheet")
