import cx_Oracle

con = None
cursor = None

def getConnection():
    try:
        global con
        global cursor
        con = cx_Oracle.connect('avik/1234567@localhost:1521/orcl1')
        return con
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)

def endConnection():
    if cursor:
        cursor.close()
    if con:
        con.close()
