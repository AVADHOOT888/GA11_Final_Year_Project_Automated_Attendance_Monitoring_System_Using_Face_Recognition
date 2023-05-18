from pytz import timezone
import pandas as pd
import datetime
import mysql.connector
import json

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

    query = f'''SELECT s.ID, s.student_name, a.attend_status \
    FROM Lectures l \
    JOIN Attendance a ON l.ID = a.LectureID \
    JOIN Students s ON a.StudentID = s.ID \
    WHERE l.ID = {x} \
    AND l.lect_date = '{cur_date}';'''

    cursor.execute(query)

    results = []
    for row in cursor.fetchall(): 
        results.append({'id': row[0], 'student_name': row[1], 'attend_status': row[2]})
    json_data = json.dumps(results)

    print(json_data)
    
  
fetchAttendance(39)




