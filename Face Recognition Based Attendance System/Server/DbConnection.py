import cv2
import face_recognition #face-recognistion
import dlib #19.18
import numpy as np
import os
from datetime import datetime
import cx_Oracle
import connection as Conn
from collections import Iterable
from io import BytesIO
import numpy as np
import io
from collections import defaultdict
from PIL import Image

name = []
img_in = []
DB_IMAGE_LIST = []  # LOAD FROM DB
DB_NAME_LIST = []  # LOAD FROM DB
DB_ROLL_LIST = []  # LOAD FROM DB


#CONVERSION METHODS
def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)


#INSERTION DATA QUERIES
def data_insertion_name(cursor,con,studentRoll,FstudentName,LstudentName,dept):
    cursor.execute("""insert into test_StudentName  (Student_ID,FNAME,LNAME,Department_id) values (:id, :fname, :lname,:dept)""",
                       id=studentRoll,fname=FstudentName, lname=LstudentName,dept=dept)
    con.commit()


def data_insertion_photo(cursor,con,studentRoll,img_data):
    cursor.execute("""insert into test_StudentPhoto  (Student_ID,Photo) values (:id, :photo)""",
            id=studentRoll, photo=img_data)
    con.commit()

def data_insertion_photoencoding(cursor,con,studentRoll,img_encode):
    cursor.execute("""insert into test_StudentEncoding  (Student_ID,PHOTO_ENCODINGS) values (:id, :photo)""",
            id=studentRoll, photo=img_encode)
    con.commit()


def data_insertion_dept(cursor,con,department,year):
    cursor.execute("""insert into test_StudentDepartment (department_id,DNAME,dyear) values (test_dept_seq.nextval,:dname,:dyear)""",
                   dname=department,dyear=year)
    con.commit()

def data_insertion_attendance(cursor,con,studentRoll):
    print("Entering Attendance")
    cursor.execute("""insert into test_StudentAttendance(ID,Student_ID,Status_Date)values(test_att_seq.nextval,:roll,CURRENT_TIMESTAMP)""",
                   roll=studentRoll)
    con.commit()

#FETCHING DATA

def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
    if default_type == cx_Oracle.DB_TYPE_BLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

def fetching_data(cursor,con):
    name=[]
    img_in=[]
    DB_IMAGE_LIST = []  # LOAD FROM DB
    DB_NAME_LIST = []  # LOAD FROM DB
    DB_ENCODE_LIST = []  # LOAD FROM DB
    DB_YEAR_LIST =[]
    con.outputtypehandler = output_type_handler
    cursor.execute("Select Student_ID from test_StudentName")
    rows=cursor.fetchall()
    length=len(rows)
    id_list=[]
    for result in rows:
        id_list.append(list(result))
    id_list=list(flatten(id_list))
    #print(id_list)
    for roll in id_list:
        #cursor.execute("select t1.fname || ' ' || t1.lname,t3.photo from test_StudentName t1, test_StudentPhoto t3 where t1.student_id=:id AND t3.student_id=:id", id=roll)
        cursor.execute(
            "select t1.fname || ' ' || t1.lname,t3.photo,t4.PHOTO_ENCODINGS,t1.Department_id from test_StudentName t1, test_StudentPhoto t3, test_StudentEncoding t4 where t1.student_id=:id AND t3.student_id=:id AND t4.student_id=:id ",id=roll)
        name, img_in ,encode_in,year= cursor.fetchone()
        x1 = np.array(Image.open(io.BytesIO(img_in)))
        x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2RGB)
        x2 = np.frombuffer(encode_in, dtype='float64')
        DB_IMAGE_LIST.append(x1)
        DB_NAME_LIST.append(name)
        DB_ENCODE_LIST.append(x2)
        DB_YEAR_LIST.append(year)
    #print(DB_NAME_LIST)
    return id_list,DB_NAME_LIST,DB_IMAGE_LIST,DB_ENCODE_LIST,DB_YEAR_LIST


def fetching_dept_data(cursor,con):
    Department_name =[]
    Department_year =[]
    cursor.execute("Select department_id from test_studentDepartment")
    rows=cursor.fetchall()
    length=len(rows)
    id_list=[]
    for result in rows:
        id_list.append(list(result))
    id_list=list(flatten(id_list))
    Details = defaultdict(list)
    for roll in id_list:
        cursor.execute("Select dname,dyear from test_studentDepartment where department_id=:id ",id=roll)
        dname,dyear= cursor.fetchone()
        Department_name.append(dname)
        Department_year.append(dyear)
    return id_list,Department_name,Department_year


#DB CONNECT METHODS

def db_connect_name(studentRoll,FstudentName,LstudentName,dept):
    try:
        global cursor
        print("Establishing Connection ........")
        con = Conn.getConnection()
        print("Connection Established Connection")
        cursor = con.cursor()
        print("Starting Queries Entry")
        data_insertion_name(cursor,con,studentRoll,FstudentName,LstudentName,dept)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")


def db_connect_photo(studentRoll,img_data):
    try:
        global cursor
        print("Establishing Connection ........")
        con = Conn.getConnection()
        print("Connection Established Connection")
        cursor = con.cursor()
        print("Starting Queries Entry")
        data_insertion_photo(cursor,con,studentRoll,img_data)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")



def db_connect_dept(department,dyear):
    try:
        global cursor
        print("Establishing Connection ........")
        con = Conn.getConnection()
        print("Connection Established Connection")
        cursor = con.cursor()
        print("Starting Queries Entry")
        data_insertion_dept(cursor,con,department,dyear)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")


def db_connect_attendance(studentroll):
    try:
        global cursor
        print("Establishing Connection ........")
        con = Conn.getConnection()
        print("Connection Established Connection")
        cursor = con.cursor()
        print("Starting Queries Entry")
        data_insertion_attendance(cursor,con,studentroll)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")




def db_connect_fetchdata_recognition():
    try:
        global cursor
        print("Establishing Connection ........")
        con = Conn.getConnection()
        print("Connection Established Connection")
        cursor = con.cursor()
        print("Starting Queries Entry")
        fetching_data(cursor,con)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")


def fetching_test_data(cursor,con):
    con.outputtypehandler = output_type_handler
    cursor.execute("SELECT PHOTO_ENCODINGS FROM test_StudentEncoding Where student_id=434120010026")
    encode_in = cursor.fetchone()
    print(encode_in.dtype)


#CHECK ATTENDANCE
import time
def fetching_attendance_data(cursor,con,fromdate,todate,did):
    print("Executing attendance Query")
    print(fromdate)
    print(todate)
    print(did)
    cursor.execute("""SELECT test_studentattendance.student_ID,test_studentname.fname|| ' ' || test_studentname.lname as name ,COUNT(*),test_studentdepartment.dname 
    FROM test_studentattendance 
    JOIN test_studentname ON test_studentattendance.student_ID=test_studentname.student_ID
    JOIN test_studentdepartment ON test_studentdepartment.department_ID=test_studentname.department_ID
    where trunc(status_date)>=TO_DATE(:fromdate, 'yyyy-mm-dd') AND 
        trunc(status_date)<TO_DATE(:todate, 'yyyy-mm-dd') AND test_studentname.department_id=:did
    GROUP BY test_studentattendance.student_ID,test_studentname.fname,test_studentname.lname,test_studentdepartment.dname""",fromdate=fromdate,todate=todate,did=did)
    rows = cursor.fetchall()
    db_rolls = []
    db_name = []
    db_count = []
    db_dept = []
    print(rows)
    for row in rows:
        db_rolls.append(row[0])
        db_name.append(row[1])
        db_count.append(row[2])
        db_dept.append(row[3])
    print(db_name)
    return db_rolls,db_name,db_count,db_dept

def fetching_attendance_data_byroll(cursor,con,fromdate,todate,rollno):
    print("Executing ateendance Query Here")
    cursor.execute("""SELECT test_studentattendance.student_ID,test_studentname.fname|| ' ' || test_studentname.lname as name ,COUNT(*),test_studentdepartment.dname 
    FROM test_studentattendance 
    JOIN test_studentname ON test_studentattendance.student_ID=test_studentname.student_ID
    JOIN test_studentdepartment ON test_studentdepartment.department_ID=test_studentname.department_ID
    where trunc(status_date)>=TO_DATE(:from_date, 'yyyy-mm-dd') AND 
        trunc(status_date)<TO_DATE(:to_date, 'yyyy-mm-dd') AND test_studentname.student_ID=:sdid
    GROUP BY test_studentattendance.student_ID,test_studentname.fname,test_studentname.lname,test_studentdepartment.dname""",
                          from_date=fromdate,to_date=todate,sdid=rollno)
    rows = cursor.fetchall()
    db_rolls=[]
    db_name = []
    db_count = []
    db_dept = []
    for row in rows:
        db_rolls.append(row[0])
        db_name.append(row[1])
        db_count.append(row[2])
        db_dept.append(row[3])
    return db_rolls,db_name,db_count,db_dept


#TESTING
def db_connect_testing():
    try:
        global cursor
        print("Establishing Connection ........")
        con = Conn.getConnection()
        print("Connection Established Connection")
        cursor = con.cursor()
        print("Starting Queries Entry")
        fetching_test_data(cursor,con)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")


def adding_student_data(cursor,con,rollno,fname,lname,dep_id,photo,photo_encoding):
    data_insertion_name(cursor, con, rollno, fname, lname, dep_id)
    data_insertion_photo(cursor, con, rollno, photo)
    data_insertion_photoencoding(cursor, con, rollno, photo_encoding)
