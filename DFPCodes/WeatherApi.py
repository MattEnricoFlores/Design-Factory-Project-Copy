import requests
import time
from datetime import datetime, timedelta
import json


def urloop():
        API_URL = f'https://iot.research.hamk.fi/api/v1/hamk/weather?place=Valkeakoski'
        now = datetime.now()
        start_time = (now - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        updated_api_url = f'{API_URL}&starttime={start_time}&endtime={end_time}&fileds=Humidity,Temperature'
        
        print(updated_api_url)

        response_API = requests.get(updated_api_url, None, verify=False)

        if response_API.status_code == 200:
            response = response_API.json()
            print(response.get("results")[0].get("series")[0].get("values")[-1][4])
            print(response.get("results")[0].get("series")[0].get("values")[-1][14])
        else:
            print(f"Failed to fetch data from API. Status code: {response_API.status_code}")


if __name__ == "__main__":
    while True:
        urloop()
        time.sleep(600)  # Sleep for 15 minutes (900 seconds)


