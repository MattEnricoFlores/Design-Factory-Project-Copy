import urllib.request
import json
import routes.api_routes as api_key


def FuckAllData():

    api_url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=10&startTime=2023-09-01T00:00:00Z&endTime=2023-09-25T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'

    # Create a request with headers
    request = urllib.request.Request(api_url, headers=api_key.headers)

    try:
        # Open the URL and read the response
        with urllib.request.urlopen(request) as response:
            data = response.read().decode('UTF-8')

        # Parse the JSON data
        parsed_data = json.loads(data)

        # Access the 'series' key
        series = parsed_data['results'][0]['series'][0]

        # Access the 'values' key to get the data points
        values = series['values']

        # Create a list to store sorted data
        sorted_data = []

        # Iterate through the data points
        for value in values:
            timestamp, temperature, humidity, co2, light, motion, vdd = value
            sorted_data.append({
                'Timestamp': timestamp,
                'Temperature': temperature,
                'Humidity': humidity,
                'CO2': co2,
                'Light': light,
                'Motion': motion,
                'VDD': vdd
            })

        # Sort the data by timestamp
        sorted_data.sort(key=lambda x: x['Timestamp'])

        # Save the sorted data to a JSON file
        with open("data.json", "w") as file:
            json.dump(sorted_data, file, indent=4)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    print(FuckAllData())