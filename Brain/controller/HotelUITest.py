import Brain.controller.urlControl as urlControl
import requests
import json
import routes.api_routes as api_key

# Room ID = (7 - 23)
# start and end time = 2023-06-04T00:00:00Z
# Fields = temperature,humidity,co2,light,motion,vdd

roomID = input("Room ID: ")
startDate = input("Start Date: ")
endDate = input("End Date: ")
fields = input("Fields: ")

API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={roomID}&startTime={startDate}&endTime={endDate}&fields={fields}'

urlControl.response_API = requests.get(API_URL,headers=config.headers,verify=False)

response = urlControl.response_API.json()

print(json.dumps(response, indent=3))
# print(HotelAPI.response_API.text)
# print(HotelAPI.response_API)

#Start Date: 2023-09-06T09:30:00Z
#End Date: 2023-09-06T09:45:00Z