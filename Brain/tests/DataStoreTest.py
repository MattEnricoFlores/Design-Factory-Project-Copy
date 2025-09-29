import urllib.request
import Brain.controller.urlControl as urlControl
import routes.api_routes as api_key

url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id=10&startTime=2023-09-14T00:00:00Z&endTime=2023-09-14T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'

# Create a request with headers
request = urllib.request.Request(url, headers=api_key.headers)

try:
    # Open the URL and read the response
    with urllib.request.urlopen(request) as response:
        data = response.read().decode('UTF-8')

    # Save the data to a JSON file (raw version)
    with open("data.json") as file:
        file.write(data)

    print("Data has been successfully saved to data.json")
except Exception as e:
    print(f"An error occurred: {str(e)}")




