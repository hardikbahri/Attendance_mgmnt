from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt



# connection with mongodb
client = MongoClient('mongodb://localhost:27017/')
db = client['Attendance_Management']
collection = db['attendance']

# if program == 1:
# fetch data from database
cursor = collection.find({})
attendance_data = list(cursor)

names = []
for record in attendance_data:
    if 'name' in record:
        names.append(str(record['name']))  # Convert to string

# Initialize attendance status for each student to an empty list
attendance_dict = {}

for name in names:
    attendance_dict[name] = []

# Extract the attendance status for each student
for record in attendance_data:
    name = record.get('name')
    status = record.get('attendance')
    date = record.get('date')
    if name is not None and status is not None:
        attendance_dict[str(name)].append((status, date))  # Store as tuple, and convert name to string

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
    
    
def report_generation_se(emp, choice, month):
    for name, count_dict in attendance_count.items():
        if name == emp and choice == 'all-time':
            # Convert name and count to numpy arrays
            n = np.array([name])
            p = np.array([count_dict['present']])
            a = np.array([count_dict['absent']])
            bar(n, p, a)  # Call bar with arrays

            sizes = [count_dict['present'], count_dict['absent']]
            pie(sizes)  # Call pie with a list

            # Extract dates and present status for the employee
            dates = [data[i] for data in attendance_dict.get(emp, []) for i in range(1, len(data), 2)]
            present = [1 if data[i] == 'present' else 0 for data in attendance_dict.get(emp, []) for i in range(0, len(data), 2)]
            line_graph(dates, present)  # Call line_graph with lists

        if name == emp and choice == 'monthly':
            dates = []
            present = []
            p_count = 0
            a_count = 0
            for data in attendance_dict.get(emp, []):
                if len(data) != 2:
                    continue
                status, date = data
                if choice == 'monthly':
                    if len(date) == 8 and date[2] == str(month):
                        dates.append(date)
                        if status == 'present':
                            present.append(1)
                            p_count += 1
                        elif status == 'absent':
                            present.append(0)
                            a_count += 1
                    elif len(date) == 9 and date[3] == str(month):
                        dates.append(date)
                        if status == 'present':
                            present.append(1)
                            p_count += 1
                        elif status == 'absent':
                            present.append(0)
                            a_count += 1

            bar(emp, p_count, a_count)  # Call bar with integers
            sizes = [p_count, a_count]
            pie(sizes)  # Call pie with a list
            line_graph(dates, present)  # Call line_graph with lists
            report_generation_se(emp, choice, month)


