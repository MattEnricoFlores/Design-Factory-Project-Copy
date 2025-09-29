import requests
import controller.urlControl as urlControl
import json
import time
from datetime import datetime, timedelta, timezone
import pytz

def fetch_data_and_print_response():
    try:
        # HotelAPI.urloop()
        now = datetime.now(pytz.utc)
        start_time = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(start_time)
        print(end_time)

        updated_api_url = f'{urlControl.API_URL}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2,light,motion,vdd'

        print(f"Request URL: {updated_api_url}")
        response_API = requests.get(updated_api_url, headers=urlControl.headers, verify=False)

        if response_API.status_code == 200:
            response = response_API.json()
            print(json.dumps(response, indent=3))
        else:
            print(f"Failed to fetch data from API. Status code: {response_API.status_code}")
    except Exception as e:
        print(f"Error while fetching data from API: {str(e)}")

if __name__ == "__main__":
    while True:
        fetch_data_and_print_response()
        time.sleep(900)  # Sleep for 15 minutes (900 seconds)

        
