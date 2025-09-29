import pyrebase
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("C:\eclipse\design_factor_project\DFPCodes\ConnectFireStore.json")
firebase_admin.initialize_app(cred)



with open("HistoryData.json", 'r') as j:
    contents = json.loads(j.read())



db = firestore.client()

collection = db.collection('programmer_details')  # create collection
res = collection.document('A01').set(contents)


# print(res)
print(res)


res = collection.document('A01').set(collection)

# collection = db.collection('programmer_details')  # create collection
# res = collection.document('A01').set({ # insert document
#     'name': 'Vishnu',
#     'age': 19,
#     'Country': 'India',
#     'Programming_languages': ['Python', 'C#', 'C++']
# })
# print(res)

# collection_ref = db.collection('Rooms').document('1')
# collection_ref.set(contents)
# for item in contents:
#         # Add data to Firestore collection
#     collection_ref.set(item)




# for item in contents:
#         # Add data to Firestore collection
#     collection_ref.set(item)
# print(item)
# def set(self, contents):
#     collection_ref = db.collection('Rooms').documnet(str(contents['id'])).set(contents)  # Use your desired Firestore collection name
#     return collection_ref
# for item in contents:
#     # Assuming 'item' is a dictionary representing a document
#     # Add data to Firestore collection
#     collection_ref.add(item)

# print("Data added to Firestore successfully")
