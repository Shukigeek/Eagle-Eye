import MySQLdb

def connect_db():
    try:
        conn = MySQLdb.connect(
            host="localhost",
            user="root",
            password="",
            database="eagleEyeDB"
        )
        print("your connected")
        return conn
    except Exception as e:
        print("failed to connect")
        print(e)
        return None




