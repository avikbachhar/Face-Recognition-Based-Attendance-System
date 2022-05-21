import DbConnection as dbconn
import connection as Conn
import cx_Oracle
from collections import defaultdict

def db_connect_fetchdata_recognition():
    try:
        global cursor
        con = Conn.getConnection()
        cursor = con.cursor()
        id_list = []
        DB_IMAGE_LIST = []  # LOAD FROM DB
        DB_NAME_LIST = []  # LOAD FROM DB
        DB_ENCODE_LIST = []  # LOAD FROM DB
        DB_YEAR_LIST = []
        id_list,DB_NAME_LIST,DB_IMAGE_LIST,DB_ENCODE_LIST,DB_YEAR_LIST=dbconn.fetching_data(cursor,con)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")
    return id_list,DB_NAME_LIST,DB_IMAGE_LIST,DB_ENCODE_LIST,DB_YEAR_LIST



def db_connect_fetchdata_department():
    try:
        global cursor
        con = Conn.getConnection()
        cursor = con.cursor()
        DYear_ID=[]
        Department_year = []
        Department_name = []
        DYear_ID,Department_name,Department_year=dbconn.fetching_dept_data(cursor,con)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")
        return DYear_ID,Department_name,Department_year


def db_connect_adddata_student(rollno,fname,lname,dep_id,photo,photo_encoding):
    try:
        global cursor
        con = Conn.getConnection()
        cursor = con.cursor()
        dbconn.adding_student_data(cursor,con,rollno,fname,lname,dep_id,photo,photo_encoding)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")


#Check Attendance
def db_connect_getattendance(fromdate,todate,did):
    db_rolls=[]
    db_name=[]
    db_count=[]
    db_dept=[]
    try:
        global cursor
        con = Conn.getConnection()
        cursor = con.cursor()
        db_rolls,db_name,db_count,db_dept=dbconn.fetching_attendance_data(cursor,con,fromdate,todate,did)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")
        return db_rolls,db_name,db_count,db_dept
def db_connect_getattendance_byroll(fromdate,todate,rollno):
    db_rolls=[]
    db_name=[]
    db_count=[]
    db_dept=[]
    try:
        global cursor
        con = Conn.getConnection()
        cursor = con.cursor()
        db_rolls,db_name,db_count,db_dept=dbconn.fetching_attendance_data_byroll(cursor,con,fromdate,todate,rollno)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")
        return db_rolls,db_name,db_count,db_dept

def db_test():
    try:
        global cursor
        con = Conn.getConnection()
        cursor = con.cursor()
        cursor.execute("""SELECT test_studentattendance.student_ID,test_studentname.fname|| ' ' || test_studentname.lname as name ,COUNT(*),test_studentdepartment.dname 
        FROM test_studentattendance 
        JOIN test_studentname ON test_studentattendance.student_ID=test_studentname.student_ID
        JOIN test_studentdepartment ON test_studentdepartment.department_ID=test_studentname.department_ID
        where trunc(status_date)>=  AND 
            trunc(status_date)<TO_DATE('2022-05-11', 'yyyy-mm-dd') AND test_studentname.department_id=1000
        GROUP BY test_studentattendance.student_ID,test_studentname.fname,test_studentname.lname,test_studentdepartment.dname""")
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

    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        cursor.close()
        Conn.endConnection()
        print("Ended Connection")


if __name__=="__main__":
    db_test()