from pymongo import MongoClient


import datetime


# connection with mongodb
client = MongoClient('mongodb://localhost:27017/')
db = client['Attendance_Management']
collection = db['attendance']

# date time module
current_datetime = datetime.datetime.now()
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day
current_hour = current_datetime.hour
current_minute = current_datetime.minute
date = str(current_day) + "/"+str(current_month)+"/"+str(current_year)
time = str(current_hour)+":"+str(current_minute)


 

# fetch data from database
cursor = collection.find({})
attendance_data = list(cursor)

# attendance registration
def attendance_registration(choice,username):
    
    x = 0
    if (choice == 'Present'):
        name = username

        for record in attendance_data:
            if record['name'] == name:
                if record['date'] == date:
                    x = 1
                    return "error you have already marked todays attendance "
                    
                    
        if (x == 0):
            
            att_dic = {"name": username, "attendance": choice, "date": date, "time": time}
            print(username)
            collection.insert_one(att_dic)
            return "attendance marked "