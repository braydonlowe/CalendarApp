import sqlite3
from sqLite import utils


def checkTableIfExists() -> bool:
    cursor, conn = utils.createCursorConn()
    try:
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='User'
        """)
        return cursor.fetchone() is not None
    except Exception as e:
        print("Tables don't exist in check table: ", e)
    finally:
        cursor.close()
        conn.close()


def createTables():
    if checkTableIfExists():
        return
    
    cursor, conn = utils.createCursorConn()
    #Else create the tables

    try:
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            canvas_url TEXT NOT NULL
        );
                             
        CREATE TABLE IF NOT EXISTS User_Semester (
            semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            semester_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        );
                            
        CREATE TABLE IF NOT EXISTS Class (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            semester_id INTEGER
        );
                            
                         
        CREATE TABLE IF NOT EXISTS Assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_name TEXT NOT NULL,
            class_id INTEGER,
            due_date DATETIME,
            completed BOOLEAN,
            FOREIGN KEY (class_id) REFERENCES Class(class_id)
        );                  
        
        """)

        conn.commit()
        print("Tables created successfully")
    except Exception as e:
        print("An error occurred while creating tables: ", e)


    finally:
        conn.close()

    