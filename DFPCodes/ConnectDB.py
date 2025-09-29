import pyrebase
import firebase as db
import json
import config
import time

def pushTheFiles():
	firebase = pyrebase.initialize_app(config.configDB)
	database = firebase.database()
	#ref = db.reference("")

	# data = 'data.json'
	# print(data)

	with open("data.json", "r") as f: #"data.json instead / "
		file_contents = json.load(f)
	#database.set(file_contents)
	print(file_contents)

	database.push(file_contents)



