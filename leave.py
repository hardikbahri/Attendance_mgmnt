import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")  
db = client["Attendance_Management"]  
collection = db["leave_approval"]



def request_leave(name, days):
    if collection.count_documents({"username": name, "days": days}) == 0:
        collection.insert_one({"username": name, "status": 0, "days": days})
        return "Request pending"
    else:
        return "Leave already requested"

    
def emp_rep(option):
    x=collection.find_one()
    if x is not None: 
        name=x['username']
        days=x['days']
        return "employee ",name ," has requested for a leave of ",days," days"
        
    if option=="yes":
        return 1,name
    else:
        return 0,name
def check_leave():
    person = collection.find_one()
    print(person["status"])
    
    if person["status"] == 0:
        message = person["username"] + " has requested a leave"
        print(str(message))  # Print the message to the console
        return str(message)  # Return the message
    else:
        return None




        
   
def approve_leave(approval):
    person=collection.find_one()
    if person["status"]==0:
        
        
        
        if approval=='yes':
                collection.insert_one({"username":person["username"],"status":1})
                collection.delete_one({"username":person["username"],"status":0})
                return "leave approved"
        if approval=='no':
                collection.delete_one({"username":person["username"]})
                return "leave disapproved"
      

def check_leave_status(name):
   
    status=collection.find_one({"username":name})
    if status is not None:
        if status['status']==1:
            collection.delete_one({"username":name,"status":1})
            return"leave approved"
            
        if status['status']==0:
            return"request pending"
        if status==None:
            return"request denied"
    

  
  