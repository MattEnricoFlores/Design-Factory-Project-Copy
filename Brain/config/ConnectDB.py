import pyrebase
import json
import config.configDB as configDB
import time

def pushTheFiles():
	# firebase = pyrebase.initialize_app(configDB.config)
	# database = firebase.database()
	#ref = db.reference("")

	# data = 'data.json'
	# print(data)

	with open("Brain\\data.json", "r") as f: #"data.json instead / "
		file_contents = json.load(f)
	#database.set(file_contents)
	print(file_contents)

	# database.set(file_contents)

pushTheFiles()

