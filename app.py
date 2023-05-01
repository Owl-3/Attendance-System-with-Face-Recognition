import streamlit as st
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


def main():
    st.title('Face Recognition Attendance system')
    prompts = ['Take attendance', 'End attendance']
    choice = st.sidebar.selectbox('Select Action', prompts)

    if choice == 'Take attendance':
        st.subheader('Attendance is being taken')
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


    elif choice == 'End attendance':
        st.subheader('Press q to end attendance')



if __name__ == '__main__':
    main()
