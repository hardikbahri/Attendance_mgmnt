import pymongo
from hashlib import sha256


client = pymongo.MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string

# Select the database and collection
db = client["Attendance_Management"]  
collection = db["users"] 
def register_user(username, password):
    if collection.count_documents({"username": username}) > 0:
        return "user already exists"
    else:
        hash_pword = sha256(password.encode()).hexdigest()
        user_doc = {
            "username": username,
            "password": hash_pword
        }
        collection.insert_one(user_doc)
        return "user registered successfully"

def login(username, password):
    if collection.count_documents({"username": username}) > 0:
        user = collection.find_one({"username": username})
        db_pword = user["password"]
        hash_pword = sha256(password.encode()).hexdigest()
        if db_pword == hash_pword:
            return "login successful"
        else:
            return "incorrect password"
    else:
        return "user not found, register first"

 

