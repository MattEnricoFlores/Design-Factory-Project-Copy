import AllDataToJsonTest
import time
import TemperatureAlert
import Co2Alert
import threading

# Define a function to run Co2Alert.alerttest() in a separate thread
def co2_alert_thread():
    while True:
        Co2Alert.alerttest()
        time.sleep(10)  # Sleep for 5 seconds
    

# Define a function to run TemperatureAlert.alerttest() in a separate thread
def temperature_alert_thread():
    while True:
        TemperatureAlert.alerttest()
        time.sleep(10)  # Sleep for 5 seconds

if __name__ == "__main__":
    # Create threads for Co2Alert.alerttest() and TemperatureAlert.alerttest()
    co2_alert_thread = threading.Thread(target=co2_alert_thread)
    temperature_alert_thread = threading.Thread(target=temperature_alert_thread)

    # Start the Co2Alert thread and the TemperatureAlert thread
    co2_alert_thread.start()
    temperature_alert_thread.start()

    while True:
        AllDataToJsonTest.urloop()
        # ConnectDB.pushTheFiles()
        time.sleep(10)  # Sleep for 5 seconds

 


# if __name__ == "__main__":
#     while True:
#         AllDataToJsonTest.urloop()
#         #ConnectDB.pushTheFiles()
#         TemperatureAlert.alerttest()
#         time.sleep(5)  # Sleep for 15 minutes (900 seconds)

