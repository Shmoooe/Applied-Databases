import pymysql

conn = None

def connect_mysql():
    global conn
    if not conn:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="blueSky73!",
            db="appdbproj",
            cursorclass=pymysql.cursors.DictCursor
            )
    return conn       
                
          