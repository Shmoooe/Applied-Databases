import pymysql

conn = None

def connect_mysql():
    global conn
    if not conn:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            db="appdbproj",
            cursorclass=pymysql.cursors.DictCursor
            )
    return conn       
                
          