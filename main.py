import requests
from datetime import datetime
import os

from requests.models import HTTPError

sheet_endpoint = "PASTE SHEETY ENDPOINT FOR YOUR SHEET HERE"
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
SHEET_TOKEN = os.environ.get("SHEET_TOKEN")


nutritionix_headers = {"x-app-id": NUTRITIONIX_APP_ID, "x-app-key": NUTRITIONIX_API_KEY}
sheet_headers = {
    "Content-Type": "application/json",
    "Authorization": SHEET_TOKEN,
}

gender = input("What is your gender? (male/female):\n>> ")
weight = float(input("How many kilograms do you weight?:\n>> "))
height = float(input("How many centimeters do you have?:\n>> "))
age = int(input("How old are you?:\n>> "))
exercise = input("What was your exercise today?:\n>> ")

nutritionix_params = {
    "query": exercise,
    "gender": gender,
    "weight_kg": weight,
    "height_cm": height,
    "age": age,
}

try:
    exercise_response = requests.post(
        url=nutritionix_endpoint, json=nutritionix_params, headers=nutritionix_headers
    )
    exercise_response.raise_for_status()
    exerciseses_json = exercise_response.json()
except HTTPError:
    print("Wrong data in .env file")


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
