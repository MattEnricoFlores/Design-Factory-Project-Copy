import RealTimeDataToJson
import config.ConnectDB as ConnectDB
import time
import DataStoreTest2

if __name__ == "__main__":
    while True:
        RealTimeDataToJson.urloop()
        RealTimeDataToJson.urloop2()
        # DataStoreTest2.main()
        #ConnectDB.pushTheFiles()
            
        time.sleep(900)  # Sleep for 15 minutes (900 seconds)
