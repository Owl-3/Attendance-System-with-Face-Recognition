import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
import streamlit
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from PIL import Image
import numpy as np
from datetime import datetime
import glob
import csv
from streamlit_option_menu import option_menu
from PIL import Image

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccount.json")
    default_app = firebase_admin.initialize_app(cred, {
        'databaseURL': "https://attendance-system-1edc5-default-rtdb.firebaseio.com/",
        'storageBucket': "attendance-system-1edc5.appspot.com"
    })
bucket = storage.bucket()

def main():
    streamlit.title('Face Recognition Attendance system')
    prompts = ['Take attendance', 'End attendance']
    choice = streamlit.sidebar.selectbox('Select Action', prompts)

    if choice == 'Take attendance':
        streamlit.subheader('Attendance is being taken')

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        imgBackground = cv2.imread('Resources/background.png')

        # Importing the mode images into a list
        folderModePath = 'Resources/Modes'
        modePathList = os.listdir(folderModePath)
        imgModeList = []
        for path in modePathList:
            imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
        # print(len(imgModeList))

        # Load the encoding file
        print("Loading Encode File ...")
        file = open('EncodeFile.p', 'rb')
        encodeListKnownWithIds = pickle.load(file)
        file.close()
        encodeListKnown, studentIds = encodeListKnownWithIds
        # print(studentIds)
        print("Encode File Loaded")

        modeType = 0
        counter = 0
        id = -1
        imgStudent = []
        students = studentIds.copy()

        now = datetime.now()
        # current_date = now.strftime("%Y-%m-%d %H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        f = open(current_date + '.csv', 'w+', newline='')
        linewriter = csv.writer(f)

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # reducing the image size to fit into the frame modes
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            imgBackground[162:162 + 480, 55:55 + 640] = img
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            # if cv2.waitKey(1) == ord('q'):
            #     break

            if faceCurFrame:
                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    # distances between matches; smallest distance, closest match
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    # print("matches", matches)
                    # print("faceDis", faceDis)
                    matchIndex = np.argmin(faceDis)
                    # print("Match Index", matchIndex) # displaying image index predicted.

                    if matches[matchIndex]:
                        # print("Known Face Detected")
                        # print(studentIds[matchIndex])
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                        id = studentIds[matchIndex]
                        if counter == 0:
                            cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                            cv2.imshow("Face Attendance", imgBackground)
                            cv2.waitKey(1)
                            counter = 1
                            modeType = 1

                if counter != 0:

                    if counter == 1:
                        # Get the Data
                        studentInfo = db.reference(f'Student/{id}').get()
                        print(studentInfo)
                        # Get the Image from the storage
                        blob = bucket.get_blob(f'Images/{id}.png')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                        # Update data of attendance
                        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                           "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                        print(secondsElapsed)
                        # ref = db.reference(f"Student/{id}")
                        # studentInfo['total_attendance'] += 1
                        # ref.child('total_attendance').set(studentInfo['total_attendance'])
                        if secondsElapsed > 30:
                            face_ids = []
                            ref = db.reference(f'Student{id}')
                            studentInfo['total_attendance'] += 1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            if matches[matchIndex]:
                                Id = studentIds[matchIndex]

                            face_ids.append(Id)
                            if Id in studentIds:
                                if Id in students:
                                    students.remove(Id)
                                    print(students)
                                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                                    linewriter.writerow([studentIds, current_time])
                        else:
                            modeType = 3
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if modeType != 3:

                        if 10 < counter < 20:
                            modeType = 2

                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        if counter <= 10:
                            # noinspection PyTypeChecker,PyUnboundLocalVariable
                            cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            # noinspection PyTypeChecker
                            cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(id), (1006, 493),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            # noinspection PyTypeChecker
                            cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            # noinspection PyTypeChecker
                            cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            # noinspection PyTypeChecker
                            cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            # noinspection PyTypeChecker
                            (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414 - w) // 2
                            # noinspection PyTypeChecker
                            cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                            imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                        counter += 1

                        if counter >= 20:
                            counter = 0
                            modeType = 0
                            studentInfo = []
                            imgStudent = []
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            else:
                modeType = 0
                counter = 0

            # cv2.imshow("Webcam", img)
            cv2.imshow("Face Attendance", imgBackground)
            cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                streamlit.text('Press q to end attendance')
                break



if __name__ == '__main__':
    main()

