import pyrebase
import json

config = {
  "apiKey": "AIzaSyAMLTOlabeqriGGYn-jALTOtqPPxjU1DjU",
  "authDomain": "testtheshit-7788a.firebaseapp.com",
  "databaseURL": "https://testtheshit-7788a-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "testtheshit-7788a",
  "Url": "https://console.firebase.google.com/project/testtheshit-7788a/db/testtheshit-7788a-default-rtdb/data/~2F",
  "storageBucket": "testtheshit-7788a.appspot.com",
  "messagingSenderId": "957364372253",
  "appId": "1:957364372253:web:9951ebcb907e18fee697f4",
  "measurementId": "G-2KE3JPZH2B"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# data = {'Age' : '30', 'Name' : 'Shreya', 'Food':'Curry'}

with open("C:\eclipse\design_factor_project\HistoryData.json", "r") as file:
        file_contents = json.load(file)
#-------------------------------------------------------------------------------
# Create Data
#print (file_contents)
database.push(file_contents)
# database.child("Users").child("FirstPerson").set(file_contents)

# #-------------------------------------------------------------------------------
# # Read Data# jenna = db.child("Users").child("FirstPerson").get()
# print(jenna.val())
# #-------------------------------------------------------------------------------
# # Update Data

#db.child("Users").child("FirstPerson").update({"Name": "Larry"})

# #-------------------------------------------------------------------------------
# # Remove Data

# #Delete 1 Value
# db.child("Users").child("FirstPerson").child("Age").remove()

# # Delete whole Node
# db.child("Users").child("FirstPerson").remove()

# def get_smallest_index(existing_data):
#     smallest_index = float('inf')  # Initialize with positive infinity
#     for key in existing_data:
        
#         # Extract the index from the data key (assuming it's a string)
#         try:
#             index = int(key)
#             if index < smallest_index:
#                 smallest_index = index
#         except ValueError:
#             pass  # Ignore keys that don't match the expected format
#     return smallest_index

# def add_data(new_index, new_data):
#     existing_data = db.child("Lobby").get().val()
#     smallest_index = get_smallest_index(existing_data)

#     if new_index < smallest_index:
#         # Delete the data with the smallest index
#         smallest_index_key = str(smallest_index)
#         db.child("Lobby").child(smallest_index_key).remove()
#         new_data_key = str(new_index)
#         db.child("Lobby").child(new_data_key).set(new_data)
#     else:
#         # Data with the new index is not smaller, so just set it
#         new_data_key = str(new_index)
#         db.child("Lobby").child(new_data_key).set(new_data)
    

# existing_data = db.child("Room 129").get().val()
# #print(existing_data)
# db.child("Room 129").child(get_smallest_index(existing_data)).remove()
