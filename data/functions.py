import sqlite3 as sql


connection_is_open = False


def connect_db(db_name):
    global connection_is_open
    while connection_is_open:
        pass
    connection_is_open = True
    db = sql.connect(db_name)
    print("Connection opened")
    return db


def close_connection(db):
    global connection_is_open
    connection_is_open = False
    print("Connection closed")
    db.close()
