import json
from datetime import datetime, timedelta
import pytz
import urllib.request
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context 
import routes.api_routes as api_key
import requests

def read_room_names():
    room_names = {}
    try:
        with open('Brain\\room_names.txt', 'r') as room_file:
            lines = room_file.readlines()
            for idx, line in enumerate(lines, start=7): 
                cleaned_line = line.strip()  # Remove leading/trailing whitespace and newline characters
                if cleaned_line:  # Check if the line is not empty
                    room_names[idx] = cleaned_line
    except FileNotFoundError:
        print("File 'room_names.txt' not found. Make sure the file exists.")
    return room_names

def urloop():
    all_data = {}  # Dictionary to store data for all rooms
    room_names = read_room_names()

    for rid, room_name in room_names.items():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        start_time = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2' #,light,motion,vdd

        print(f"Request URL: {updated_api_url}")

        try:
            # Open the URL 
            request = urllib.request.Request(updated_api_url, headers=api_key.headers)
            response = urllib.request.urlopen(request)
            # Check if the connection is ok
            if response.status == 200:
                # Read the response from url without parsing it as JSON
                data = response.read().decode('UTF-8')
                print(data)
                
                # Parse the data and store it in a list
                parsed_data = json.loads(data)
                series = parsed_data['results'][0]['series'][0]
                values = series['values']
                room_data = []
                for value in values:
                    timestamp, temperature, humidity, co2 = value

                    # Convert UTC timestamp to correct UTC, handling both cases with or without milliseconds
                    try:
                        utc_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
                    except ValueError:
                        # Fallback for timestamps without milliseconds
                        utc_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)

                    local_timestamp = utc_timestamp.astimezone(pytz.timezone("Europe/Helsinki"))
                    timestamp_utc_plus_2 = local_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                    room_data.append({
                        'Timestamp': timestamp_utc_plus_2,
                        'Temperature': temperature,
                        'Humidity': humidity,
                        'CO2': co2,
                        # 'Light': light,
                        # 'Motion': motion,
                        # 'VDD': vdd
                    })
                # Store the room data in the dictionary
                all_data[room_name] = room_data

            else:
                print(f"Failed to fetch data from API. Status code: {response.status}")
        except Exception as e:
            print(f"An error occurred: {e}")

      # Save all raw data to a single-line JSON file
    with open("Brain\\data.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))

def urloop2():

    all_data = {}
    API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/weather?place=Valkeakoski'
    now = datetime.now()
    start_time = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    updated_api_url = f'{API_URL}&starttime={start_time}&endtime={end_time}&fileds=Humidity,Temperature'
        
    print(updated_api_url)
    response_API = requests.get(updated_api_url, None, verify=False)
    

    if response_API.status_code == 200:
        response = response_API.json()
        humidity = int(response.get("results")[0].get("series")[0].get("values")[-1][4])
        temperature = int(response.get("results")[0].get("series")[0].get("values")[-1][14])
        all_data['humidity'] = humidity
        all_data['temperature'] = temperature
        print(f"Humidity: {humidity}")
        print(f"Temperature: {temperature}")
    else:
        print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

    # Write data to a JSON file
    with open("Brain\\weather.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))
urloop()
urloop2()
