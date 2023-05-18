import os
from os import listdir
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
import numpy as np
import pickle
import cv2
import base64
from keras_facenet import FaceNet
import openpyxl
from pytz import timezone
import pandas as pd
import datetime
from IPython.display import display, Javascript
from base64 import b64decode
from IPython.display import Image
# from Main import findFaces
from flask import Flask, request
from flask_cors import CORS
import mysql.connector
import json
from pytz import timezone
import pandas as pd
import datetime
import mysql.connector
import time
import logging
# from database import students

port_no = 5000
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/upload-image', methods=['POST'])
def process_image():
    try:
        file = request.files['file']
        # Process the image file here
        filename = file.filename
        file.save(os.path.join('uploads', filename))
        id_lec = finalCall(filename)
        data = fetchAttendance(id_lec)
        os.remove(os.path.join('uploads', filename))
        return {'data': data}
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return {'error': 'Image processing failed.'}


MyFaceNet = FaceNet()
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

database = {}
folder = 'Students2/Images/'
students = []


for filename in listdir(folder):
    path = folder + filename
    gbr1 = cv2.imread(path)
    if(gbr1 is not None):
        students.append(filename.split(".")[0])

    if gbr1 is None:
        print(f"Error reading image {filename}")
        continue

    wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)
    if len(wajah) == 0:
        print(f"No face detected in image {filename}")
        continue

    x1, y1, width, height = wajah[0]
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height

    gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
    gbr = Img.fromarray(gbr)
    gbr_array = np.array(gbr)

    face = gbr_array[y1:y2, x1:x2]
    face = Img.fromarray(face)
    face = face.resize((160, 160))
    face = np.array(face)

    face = np.expand_dims(face, axis=0)
    signature = MyFaceNet.embeddings(face)

    database[os.path.splitext(filename)[0]] = signature


myfile = open("data.pkl", "wb")
pickle.dump(database, myfile)
myfile.close()

myfile = open("data.pkl", "rb")
database = pickle.load(myfile)
myfile.close()

# print(database)


def js_to_image(js_reply):
    image_bytes = b64decode(js_reply.split(',')[1])
    jpg_as_np = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img


def fetchAttendance(lecId):
    connection = mysql.connector.connect(
        host='attendance-system.cepf8h0tkttq.ap-south-1.rds.amazonaws.com',
        database='attendanceSystem',
        user='admin',
        password='studentdata2023'
    )

# Execute the SQL query
    cursor = connection.cursor()
    x = lecId
    cur_date = str(datetime.date.today().strftime('%Y-%m-%d'))
    print(cur_date)
    print(x)

    query = f'''SELECT s.ID, s.student_name, a.attend_status \
    FROM Lectures l \
    JOIN Attendance a ON l.ID = a.LectureID \
    JOIN Students s ON a.StudentID = s.ID \
    WHERE l.ID = {x} \
    AND l.lect_date = '{cur_date}';'''

    cursor.execute(query)

    results = []
    for row in cursor.fetchall():
        results.append(
            {'id': row[0], 'student_name': row[1], 'attend_status': row[2]})
    json_data = json.dumps(results)

    print(json_data)
    return json_data


def rds(students, present_list):
    day_of_week = datetime.datetime.today().strftime('%A')
    # current_time = datetime.datetime.now().time()
    current_time = datetime.datetime.now(timezone("Asia/Kolkata")).time()
    print(current_time)

    # Read timetable from CSV file
    timetable = pd.read_csv('timetableTest.csv')
    current_subject = None

    # Determine the current subject based on the day of the week and time
    schedule = timetable.loc[timetable['Day'] == day_of_week]
    print(schedule)
    for i, row in schedule.iterrows():
        start_time = datetime.datetime.strptime(
            row['Timing'].split(' - ')[0], '%I:%M %p').time()
        end_time = datetime.datetime.strptime(
            row['Timing'].split(' - ')[1], '%I:%M %p').time()
        if start_time <= current_time <= end_time:
            current_subject = row['Subject']
            break

    if current_subject is None:
        print('No class is currently in session.')
        return

    # Connect to MySQL database
    try:
        connection = mysql.connector.connect(host='attendance-system.cepf8h0tkttq.ap-south-1.rds.amazonaws.com',
                                             database='attendanceSystem',
                                             user='admin',
                                             password='studentdata2023')
        cursor = connection.cursor()

        # Get subject ID from Subjects table
        cursor.execute(
            f"SELECT ID FROM Subjects WHERE subject_name = '{current_subject}'")
        print(current_subject)
        subject_id = cursor.fetchone()[0]

        # Insert lecture into Lectures table
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        cursor.execute(
            f"INSERT INTO Lectures (SubjectID, lect_date, lect_time) VALUES ({subject_id}, '{current_date}', '{current_time}')")
        lecture_id = cursor.lastrowid
        print("Lecture_Id", lecture_id)
        # Insert attendance data into Attendance table
        for student in students:
            if student == 'unknown':
                continue
            else:
                present = 1 if student in present_list else 0
                absent = 1 - present
            cursor.execute(
                f"SELECT ID FROM Students WHERE student_name = '{student}'")
            print(student)
            student_id = cursor.fetchone()[0]
            print(student_id)
            cursor.execute(
                f"INSERT INTO Attendance (LectureID, StudentID, attend_status) VALUES ({lecture_id}, '{student_id}', '{'present' if present else 'absent'}')")

        connection.commit()
        print("Attendance data saved to database.")

    except mysql.connector.Error as error:
        print(f"Error while connecting to MySQL: {error}")

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection closed.")
    return lecture_id


def findFaces(data, threshold=1):
    gbr1 = js_to_image(data)
    gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
    gbr = Img.fromarray(gbr)
    gbr_array = asarray(gbr)

    wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)
    present_Students = []
    accuracies = []
    for (x1, y1, w, h) in wajah:
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h

        face = gbr_array[y1:y2, x1:x2]

        face = Img.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)

        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)

        min_dist = 100
        identity = 'unknown'
        for key, value in database.items():
            dist = np.linalg.norm(value - signature)
            if dist < min_dist:
                min_dist = dist
                identity = key
            if min_dist > threshold:
                identity = 'unknown'

        accuracy = (threshold - min_dist) / threshold
        accuracies.append(accuracy)

        present_Students.append(identity)

        cv2.putText(gbr1, identity, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)

    filename = 'photo.jpg'
    cv2.imwrite(filename, gbr1)
    print(present_Students)
    id = rds(students, present_Students)

    return id


def findFacesFromLocalFile(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    data = "data:image/jpeg;base64," + encoded_string
    return findFaces(data, threshold=1)


####Main Code######
def take_photo(file):
    filename = findFacesFromLocalFile(f"uploads/{file}")
    return filename
##################


def finalCall(file):
    try:
        lecture_id = take_photo(file)

        display(Image(filename))
        return lecture_id
    except Exception as err:
        print(str(err))


if __name__ == '__main__':
    app.run()
