# Face Recognition Attendance System
This is a face recognition attendance system that uses computer vision and deep learning to recognize faces and record attendance. The system is designed to simplify the attendance-taking process and improve accuracy by eliminating the need for manual input and reducing the risk of errors.


Getting Started
Prerequisites
Before you can use the system, you will need to have the following installed:

Python 3.7 or later
OpenCV
NumPy
face_recognition
Pandas
Installing
To install the necessary packages, you can use pip:

Run the code
pip install CMake
pip install dlib
pip install opencv-python
pip install numpy
pip install face_recognition
pip install pandas

To run the above dependencies, execute this code in the terminals "pip3 install -r requirements.txt"
Usage
To use the system, follow these steps:

Add images of the individuals you want to recognize to the "Images" folder.
Run the "EncodeGenerator.py" script to encode the faces and store them in the "encodings" folder.
Run the "main.py" script to start the attendance system.
When a recognized face is detected, the system will mark the attendance and store it in the "attendance.csv" file.
Built With
Python - The programming language used
OpenCV - Computer vision library
NumPy - Library for numerical computations
face_recognition - Face recognition library
Pandas - Data analysis library </br></br>

### When the webcam is active


![Active](https://user-images.githubusercontent.com/84917593/235348921-62e746db-5f42-40f7-9edf-de554fe33750.png)

### The profile + marked attendance count
![Student attendance profile](https://user-images.githubusercontent.com/84917593/235348944-85a14b07-a68f-4822-83b0-936306ba7b9e.png)

</br></br>



Authors
Odira Dancan -
License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Acknowledgments
ageitgey/face_recognition for the face recognition library
opencv-python-tutroals for the OpenCV tutorials.
