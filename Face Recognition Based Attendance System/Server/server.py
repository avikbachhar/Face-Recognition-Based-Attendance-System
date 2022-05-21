from flask import Flask,render_template,Response,request,redirect,jsonify,json
import cv2
import numpy as np
import os
from datetime import datetime
import face_recognition
from werkzeug.utils import secure_filename
import DbConnection as dbconn
import connection as Conn
import ser_db as sdb
import cx_Oracle
from flask_cors import CORS
import base64
import json

app=Flask(__name__)
CORS(app)



images = []
classnames = []
studentrolls=[]
encodeListKnown=[]
studentYear=[]
Department_name=[]
Department_year=[]
DYear_ID=[]
Dept=[]
Year=[]
#Attendance
presentAttendeID=[]
presentAttendeName=[]
matchCheckIndex=[]

def markAttendance(name,id,cursor,con):
    if id not in presentAttendeID:
        presentAttendeID.append(id)
        presentAttendeName.append(name)
        dbconn.data_insertion_attendance(cursor,con,id)
    print(presentAttendeName)




@app.route('/attendes')
def attendes():
    response = jsonify({
        'studentnames': presentAttendeName
    })
    response.headers.add('Access-Control-Allow-Origin','*')

    return response

def generate_frames():
    global camera
    global cursor
    con = Conn.getConnection()
    cursor = con.cursor()
    camera = cv2.VideoCapture(0)
    while (camera.isOpened()):
        success, img = camera.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
            """Return a list of all known distances lowest is the match"""
            #print(faceDist)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                name = classnames[matchIndex].upper()
                id=studentrolls[matchIndex]
                print(name)
                y1, x2, y2, x1 = faceLoc  # Bounding Box
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name,id,cursor,con)
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',img)
            img = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n') #openCV Documentaition


@app.route('/video-terminate')
def video_terminate():
    camera.release()
    cursor.close()
    Conn.endConnection()

    print("Done")
    response = jsonify({
        'Status': "Done"
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype="multipart/x-mixed-replace;boundary=frame")

@app.route('/checkdetails', methods=['GET', 'POST'])
def checkDetails():
    print(studentrolls)
    id = request.form["id"]
    rollid=int(id)
    if rollid in studentrolls:
        dname="MCA20"
        index=studentrolls.index(rollid)
        print(index)
        ret_name=classnames[index]
        print(ret_name)
        fname_ret,lname_ret=ret_name.split(" ")
        #image process
        img=images[index]
        _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        im=str(im_b64)
        im = im[2:]
        size = len(im)
        im= im[:size - 1]
        # image process
        response = jsonify({
            'Ststatus': 1,
            'fname' : fname_ret,
            'lname' : lname_ret,
            'img' : im,
            'dname': dname
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response
    else:
        response = jsonify({
            'Ststatus': 0,
            'message' : "Student Not Found"
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response


@app.route('/getdepartments', methods=['GET', 'POST'])
def getDepartments():
    print(DYear_ID)
    Dept = []
    Year = []
    for i in range(0,len(DYear_ID)):
        Dept.append(Department_name[i])
        Year.append(Department_year[i])
    response = jsonify({
        'Dept': Dept,
        'Year': Year

    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/getdepartmentnames', methods=['GET', 'POST'])
def getDepartmentsnames():
    print(DYear_ID)
    Dept = []
    Year = []
    for i in range(0,len(DYear_ID)):
        Dept.append(Department_name[i])
    print(Dept)
    response = jsonify({
        'Dept': Dept,
        'DYear_ID': DYear_ID

    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


#Dept=['MCA','BTECH','MCA','MTECH','BBA']
#Year=[2018,2022,2023,2019,2020]
@app.route('/adddepartments',methods=['POST','GET'])
def adddepartments():
     res_dname=request.form["dname"]
     res_dyear =request.form["dyear"]
     if res_dname not in Department_name:
         last_year = DYear_ID[-1] + 1
         DYear_ID.append(last_year)
         Department_name.append(res_dname)
         Department_year.append(res_dyear)
         #TRY TO CREATE THREAD LATER
         #dbconn.db_connect_dept(res_dname,res_dyear)
         response = jsonify({
             'Ststatus': 0,
             'message': "Department Added"
         })
         response.headers.add('Access-Control-Allow-Origin', '*')
         print(response)
         return response
     else:
         response = jsonify({
             'Ststatus': 1,
             'message': "Department Name Already Exist"
         })
         response.headers.add('Access-Control-Allow-Origin', '*')
         print(response)
         return response



@app.route('/addstudentdetails', methods=['GET', 'POST'])
def addstudentdetails():
    fname = request.form["fname"]
    lname = request.form["lname"]
    rollno = request.form["rollno"]
    depID = request.form["depID"]
    img = request.form["img"]
    print(img)
    roll = int(rollno)
    if roll not in studentrolls:
        img_encode,img_db=data_conversion(img)
        try:
            encode = face_recognition.face_encodings(img_encode)[0]
        except:
            response = jsonify({
                'Ststatus': 0,
                'message': "Face Not Found Choose Different Image"
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(response)
            return response
        img_encode_db=encode.tobytes()
        images.append(img_encode)
        classnames.append(fname+" "+lname)
        studentrolls.append(roll)
        encodeListKnown.append(face_recognition.face_encodings(img_encode)[0])
        sdb.db_connect_adddata_student(roll,fname,lname,depID,img_db,img_encode_db)
        # ADD DB QUERY
        # ADD DB QUERY
        response = jsonify({
            'Ststatus': 0,
            'message': "Everything Looks Good "
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response
    else:
        response = jsonify({
            'Ststatus': 0,
            'message': "Roll Number Already Exist"
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response

def data_conversion(img):
    img_=img
    baseurl=img_[23:]
    print(baseurl)
    im_bytes = base64.b64decode(baseurl)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img_final = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR) #numpyformat
    success, encoded_image = cv2.imencode('.png', img_final)
    content2 = encoded_image.tobytes() #f.read format
    return img_final,content2

##CHECK ATTENDANCE

@app.route('/checkattendance', methods=['GET', 'POST'])
def get_student_attendance():
    fdate = request.form["fdate"]
    tdate = request.form["tdate"]
    depID = request.form["dept"]
    rollno = request.form["rollno"]
    if rollno =='':
        print("STEP 1")
        db_rolls,db_name,db_count,db_dept=sdb.db_connect_getattendance(fdate,tdate,depID)
        response = jsonify({
            'Ststatus': 1,
            'db_rolls': db_rolls,
            'db_name': db_name,
            'db_count': db_count,
            'db_dept': db_dept

        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response
    else:
        print("STEP 2")
        rollno = int(rollno)
    if rollno not in studentrolls:
        response = jsonify({
            'Ststatus': 0,
            'message' : "Student Not Found"
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response
    elif rollno in studentrolls:
        print("STEP 3")
        db_rolls,db_name,db_count,db_dept=sdb.db_connect_getattendance_byroll(fdate,tdate,rollno)
        response = jsonify({
            'Ststatus': 1,
            'db_rolls': db_rolls,
            'db_name': db_name,
            'db_count': db_count,
            'db_dept': db_dept

        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response
    else:
        print('Ye kya kar raha h bhai')
        print(rollno)
        print(type(rollno))



if __name__=="__main__":
    studentrolls, classnames, images, encodeListKnown,studentYear = sdb.db_connect_fetchdata_recognition()
    DYear_ID,Department_name,Department_year=sdb.db_connect_fetchdata_department()
    print("Starting Server....")
    app.run(debug=False)
