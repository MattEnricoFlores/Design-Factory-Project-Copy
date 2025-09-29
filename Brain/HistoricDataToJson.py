
import requests
import json
import routes.api_routes as api_key
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import pytz
import urllib.request
import ssl 

ssl._create_default_https_context = ssl._create_unverified_context

def read_room_names():
    room_names = {}
    try:
        with open('Brain//room_names.txt', 'r') as room_file:
            lines = room_file.readlines()
            for idx, line in enumerate(lines, start=7): 
                cleaned_line = line.strip()  # Remove leading/trailing whitespace and newline characters
                if cleaned_line:  # Check if the line is not empty
                    room_names[idx] = cleaned_line
    except FileNotFoundError:
        print("File 'room_names.txt' not found. Make sure the file exists.")
    return room_names
def urloop_24_hours():
    all_data = {}  # Dictionary to store data for all rooms
    room_names = read_room_names()
    
    for rid, room_name in room_names.items():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        date = now + relativedelta(hours=-24)
        start_time = (date).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=api_key.headers, verify=False)

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
                    })

                # Store the room data in the dictionary
                all_data[room_name] = room_data
            else:
                print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    with open("HistoryUI/HistoricData24Hours.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))

def urloop_1_week():
    all_data = {}  # Dictionary to store data for all rooms
    room_names = read_room_names()
    
    for rid, room_name in room_names.items():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        date = now + relativedelta(weeks=-1)
        start_time = (date).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=api_key.headers, verify=False)

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
                    })

                # Store the room data in the dictionary
                all_data[room_name] = room_data
            else:
                print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    with open("HistoryUI/HistoricData1Week.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))

def urloop_1_month():
    all_data = {}  # Dictionary to store data for all rooms
    room_names = read_room_names()
    
    for rid, room_name in room_names.items():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        date = now + relativedelta(months=-1)
        start_time = (date).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=api_key.headers, verify=False)

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
                    })

                # Store the room data in the dictionary
                all_data[room_name] = room_data
            else:
                print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    with open("HistoryUI/HistoricData1Month.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))


def urloop_6_months():
    all_data = {}  # Dictionary to store data for all rooms
    room_names = read_room_names()
    
    for rid, room_name in room_names.items():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        date = now + relativedelta(months=-6)
        start_time = (date).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=api_key.headers, verify=False)

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
                    })

                # Store the room data in the dictionary
                all_data[room_name] = room_data
            else:
                print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    with open("HistoryUI/HistoricData6Months.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))


def urloop_1_year():
    all_data = {}  # Dictionary to store data for all rooms
    room_names = read_room_names()
    
    for rid, room_name in room_names.items():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        date = now + relativedelta(months=-24)
        start_time = (date).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=api_key.headers, verify=False)

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
                    })

                # Store the room data in the dictionary
                all_data[room_name] = room_data
            else:
                print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    with open("HistoryUI/HistoricData1year.json", "w") as file:
        json.dump(all_data, file, separators=(',', ':'))

if __name__ == "__main__":
    while True:
        urloop_24_hours()
        urloop_1_week()
        urloop_1_month()
        urloop_6_months()
        urloop_1_year()
        time.sleep(900)  # Sleep for 15 minutes (900 seconds)
