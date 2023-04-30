import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-1edc5-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-system-1edc5.appspot.com"
})

# creating Student database reference to the realtime db on firebase
ref = db.reference('Student')

# storing data in json format in the firebase with student information
data = {
    "001":
        {
            "name": "Elon Musk",
            "major": "Robotics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-03-11 00:54:34"
        },
    "002":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2023-03-11 00:54:34"
        },
    "003":
        {
            "name": "Odira Dancan",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 23,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-03-03 00:54:34"
        },
    "004":
        {
            "name": "Kevin Onyancha",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 23,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-03-11 00:54:34"
        }
}

# sending the data to the firebase in realtime
for key, value in data.items():
    ref.child(key).set(value)
