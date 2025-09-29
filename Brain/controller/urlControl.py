import requests
import json
import routes.api_routes as api_key
import time
from datetime import datetime, timedelta
import pytz

def urloop():
    for rid in range(7,24):
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={rid}'
        now = datetime.now(pytz.utc)
        start_time = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2,light,motion,vdd'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=api_key.headers, verify=False)

        if response_API.status_code == 200:
            response = response_API.json()
            print(json.dumps(response, indent=3))
        else:
            print(f"Failed to fetch data from API. Status code: {response_API.status_code}")

#if __name__ == "__main__":
#    while True:
#        urloop()
#        time.sleep(900)  # Sleep for 15 minutes (900 seconds)

