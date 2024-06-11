from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import datetime
import login_page
import leave_approval
import tkinter as tk
from tkinter import messagebox
import PySimpleGUI as sg

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


# login /register

choice = input("login or register ")
username = input("enter username")
password = input("enter password ")
if choice == 'login':
    program = login_page.login(username, password)
if choice == "register":
    login_page.register_user(username, password)

# if program == 1:
# fetch data from database
cursor = collection.find({})
attendance_data = list(cursor)


# attendance registration
def attendance_registration():
    choice = input("do you wish to mark you attendance(y or n)")
    x = 0
    if (choice == 'y'):
        name = username

        for record in attendance_data:
            if record['name'] == name:
                if record['date'] == date:
                    print("error you have already marked todays attendance ")
                    x = 1
                    break
        if (x == 0):
            att = input("mark your attendance ")
            att_dic = {"name": name, "attendance": att, "date": date, "time": time}
            collection.insert_one(att_dic)


# if program == 1:
#     attendance_registration()
names = []
for record in attendance_data:
    if 'name' in record:
        names.append(record['name'])


attendance_dict = {}


#  Initialize attendance status for each student to an empty list
for name in names:
    attendance_dict[name] = []


# Extract the attendance status for each student
for record in attendance_data:
    name = record.get('name')
    status = record.get('attendance')
    date = record.get('date')
    if name is not None and status is not None:
        attendance_dict[name].append(status)
        attendance_dict[name].append(date)


# Initialize attendance count for each student
attendance_count = {}


# Count the occurrences of 'present' and 'absent' for each student
for name, status_list in attendance_dict.items():
    present_count = status_list.count('present')
    absent_count = status_list.count('absent')
    attendance_count[name] = {
        'present': present_count,
        'absent': absent_count
    }


# Print the attendance count for desired student
emp = username


# graph functions


def bar(x, y1, y2):

    plt.bar(x, y1, label='Present', color='green')
    plt.bar(x, y2, bottom=y1, label='Absent', color='red')
    plt.show()


def pie(sizes):
    plt.xlabel('Student Names')
    plt.ylabel('Attendance Count')
    plt.title('Attendance Count for Each Student')
    plt.legend()

    labels = ['Present', 'Absent']

    colors = ['green', 'red']
    plt.pie(sizes, labels=labels, colors=colors)
    plt.show()


def line_graph(x, y):
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('Dates')
    plt.ylabel('Present')
    plt.title('Present Status Over Time')
    plt.show()


def report_generation_se(emp,choice):
    for name, count_dict in attendance_count.items():
        if name == emp and choice == 'all-time':
        #print(f"{name}: Present - {count_dict['present']}, Absent - {count_dict['absent']}")
        # Convert name and count to numpy arrays
            n = np.array([name])
            p = np.array([count_dict['present']])
            a = np.array([count_dict['absent']])
            dates = []
            present = []
            for name, data in attendance_dict.items():
                if name == emp:
                    for i in range(1, len(data), 2):
                        dates.append(data[i])
                    for i in range(0, len(data), 2):
                        if data[i] == 'present':
                            present.append(1)
                        if data[i] == 'absent':
                            present.append(0)
            print(present)
            present = np.array(present)
            dates = np.array(dates)

            bar(n, p, a)
            sizes = [count_dict['present'], count_dict['absent']]
            pie(sizes)
            line_graph(dates, present)
    # Label the chart and show the legend

        if name == emp and choice == 'monthly':
            month = int(input("enter the month in numbers "))
            dates = []
            present = []
            p_count = 0
            a_count = 0
            for name, data in attendance_dict.items():
                if name == emp:
                    for i in range(1, len(data), 2):

                        if len(data[i]) == 8:
                            if data[i][2] == str(month):
                                dates.append(data[i])
                                if data[i-1] == 'present':
                                    present.append(1)
                                    p_count += 1
                                if data[i-1] == 'absent':
                                    present.append(0)
                                    a_count += 1
                        if len(data[i]) == 9:
                            if data[i][3] == str(month):
                                dates.append(data[i])
                                if data[i-1] == 'present':
                                    present.append(1)
                                    p_count += 1
                                if data[i-1] == 'absent':
                                    present.append(0)
                                    a_count += 1

            try:
                bar(emp, p_count, a_count)
                sizes = [p_count, a_count]
                pie(sizes)
                dates = np.array(dates)
                present = np.array(present)
                line_graph(dates, present)
            except:
                print("error")
     
# report_generation_se(emp,choice)
# leave_approval.request_leave(username)
# leave_approval.check_leave_status(username)
# x=leave_approval.emp_rep(3,name)
# if x==1:
#     report_generation_se(emp,choice)

# leave_approval.approve_leave(name)



class employee:
    if username!="admin":
        attendance_registration()
        choice = input("choose the type of report- monthly, department-wise or all- time ")
        report_generation_se(emp,choice)
        leave_approval.request_leave(username)
        leave_approval.check_leave_status(username)
    
class admin:
    if username=="admin":
        x,emp=leave_approval.emp_rep()
        
        
        if x==1:
            choice = input("choose the type of report- monthly, department-wise or all- time ")
            report_generation_se(emp,choice)
        leave_approval.approve_leave(name)





