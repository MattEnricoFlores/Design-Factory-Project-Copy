import json
import time
from datetime import datetime, timedelta
import requests
import courier_key
from trycourier import Courier

client = Courier(auth_token=courier_key.auth_token)
start_time = time.time()
room_counters = {}

# Function to fetch the outside temperature
def get_outside_temperature():
    API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/weather?place=Valkeakoski'
    now = datetime.now()
    start_time = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    updated_api_url = f'{API_URL}&starttime={start_time}&endtime={end_time}&fileds=Temperature'

    response_API = requests.get(updated_api_url, None, verify=False)

    if response_API.status_code == 200:
        response = response_API.json()
        return response.get("results")[0].get("series")[0].get("values")[-1][14]
    else:
        print(f"Failed to fetch data from API. Status code: {response_API.status_code}")
        return None

# Function to determine the threshold values based on outside temperature
def determine_threshold(outside_temperature):
    if -15 <= outside_temperature <= 0:
        return (21, 23)
    elif 1 <= outside_temperature <= 5:
        return (21, 24)
    elif 6 <= outside_temperature <= 10:
        return (21, 25)
    elif outside_temperature >= 15:
        return (21, 27)
    else:
        # Default threshold values if outside temperature is not in any specified range
        return (21, 23)

def alerttest():
    global start_time  # Use the global start_time variable
    while True:
        outside_temperature = get_outside_temperature()
        if outside_temperature is not None:
            threshold_values = determine_threshold(outside_temperature)
            print(f"Outside Temperature: {outside_temperature}°C, Threshold Values: {threshold_values}")

            with open("data.json", "r") as f:
                file_contents = json.load(f)

            room_temperatures = {}  # Dictionary to store room temperatures

            for room, data in file_contents.items():
                if isinstance(data, list) and data:
                    if room not in room_counters:
                        room_counters[room] = 0

                    for timestamp_data in data:
                        temperature = timestamp_data.get("Temperature")
                        if temperature is not None:
                            print(f"Room {room}: Temperature = {temperature}, Counter = {room_counters[room]}")

                            # Check if the temperature is outside the threshold range
                            if temperature < threshold_values[0] or temperature > threshold_values[1]:
                                room_counters[room] += 1

                            # Store the temperature for the room
                            room_temperatures[room] = temperature
                            break  # Break out of the loop after finding the first temperature

            elapsed_time = time.time() - start_time
            if elapsed_time >= 900:
                for room in room_counters:
                    room_counters[room] = 0
                start_time = time.time()

            for room, counter in room_counters.items():
                if counter >= 96:
                    send_alert(room, threshold_values, room_temperatures[room])

        time.sleep(10)  # Sleep for 15 minutes


def send_alert(room, threshold_values, temperature):
    min_threshold, max_threshold = threshold_values
    print(f"Alert: Temperature in Room {room} is outside the threshold range! Min = {min_threshold}, Max = {max_threshold}, Temperature = {temperature}°C")

    resp = client.send_message(
        message={
            "to": {
                "email": "mattsmttest@gmail.com"
            },
            "template": "060X6ETA1P4XFKQWH5WE29464XZK",
            "data": {
                "variables": "Alert!",
                "body": f"Alert: Temperature in Room {room} is outside the threshold range! Min = {min_threshold}, Max = {max_threshold}, Temperature = {temperature}°C",
            "content": {
                "body": f"Alert: Temperature in Room {room} is outside the threshold range! Min = {min_threshold}, Max = {max_threshold}, Temperature = {temperature}°C"
            }
            },
        }
    )

    print(resp['requestId'])

if __name__ == "__main__":
    room_counters = {}
    start_time = time.time()
    alerttest()