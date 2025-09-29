import json
import time
from email.mime.text import MIMEText
import courier_key
from trycourier import Courier

client = Courier(auth_token=courier_key.auth_token)


def alerttest():

    # Define the threshold values as a tuple (min_value, max_value)
    threshold_values = 550  # Change these values to your desired thresholds

    # Initialize a dictionary to store counters for each room
    room_counters = {}

    room_co2 = {}  # Dictionary to store room temperatures

    # Initialize the start_time variable
    start_time = time.time()

    while True:
        with open("data.json", "r") as f:
            file_contents = json.load(f)

        for room, data in file_contents.items():
            if isinstance(data, list) and data:
                if room not in room_counters:
                    room_counters[room] = 0

                for timestamp_data in data:
                    co2 = timestamp_data.get("CO2")
                    if co2 is not None:
                        print(f"Room {room}: CO2 = {co2}, Counter = {room_counters[room]}")
                        
                        # Check if the temperature is outside the threshold range
                        if co2 < threshold_values:
                            room_counters[room] += 1

                        # Store the temperature for the room
                        room_co2[room] = co2
                        break  # Break out of the loop after finding the first temperature

        # Check if 15 minutes (900 seconds) have passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= 900:
            # Reset the counters for each room and timer
            for room in room_counters:
                room_counters[room] = 0
            start_time = time.time()

        # Check if the counter for any room reaches a certain value (e.g., 3)
        for room, counter in room_counters.items():
            if counter >= 96:
                # Send an alert for the specific room (You can replace this with your preferred method of alerting)
                send_alert(room, threshold_values, room_co2[room])

        # Sleep for 15 minutes before the next iteration
        time.sleep(10)

def send_alert(room, threshold_values, co2):
    # You can implement your alerting logic here, such as sending an email, notification, or any other desired action.
    print(f"Alert: CO2 in Room {room} is outside the threshold range! Threshold = {threshold_values}, CO2 Value = {co2}")
    
    client = Courier(auth_token="pk_prod_N25BNTP81MM2Q4MDSG0HKYABTR9C")

    resp = client.send_message(
        message={
            "to": {
                "email": "mattsmttest@gmail.com"
            },
            "template": "060X6ETA1P4XFKQWH5WE29464XZK",
            "data": {
                "variables": "Alert!",
                "body": f"Alert: CO2 in Room {room} is outside the threshold range! Threshold = {threshold_values}, CO2 Value = {co2}",
            "content": {
                "body": f"Alert: CO2 in Room {room} is outside the threshold range! Threshold = {threshold_values}, CO2 Value = {co2}"
            }
            },
            
        }
    )

    print(resp['requestId'])



if __name__ == "__main__":
    alerttest()