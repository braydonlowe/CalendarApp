import sqlite3
from sqLite import create_tables
import bcrypt


def createCursorConn() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    conn = sqlite3.connect("calendarApp.db")
    cursor = conn.cursor()
    return cursor, conn


def validate_user(username: str, password: str) -> bool:
    cursor, conn = createCursorConn()

    try:
        cursor.execute("""
            SELECT password FROM User WHERE username = ?
        """, (username,))
        result = cursor.fetchone()

    except sqlite3.Error as e:
        print(f"Database error validate user: {e}")
        return False
    
    finally:
        conn.close()
    
    if result is None:
        return False
    
    hashed_password = result[0]

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)



def create_user(username: str, password: str, canvas_url: str) -> None:
    cursor, conn = createCursorConn()

    hashed_pass = hash_password(password)
    try:

        cursor.execute("""
            INSERT INTO User (username, password, canvas_url)
            VALUES (?, ?, ?)
        """, (username, hashed_pass, canvas_url))

        conn.commit()

    except sqlite3.Error as e:
        return
    finally:
        conn.close()



def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def create_semester(semester_name: str):
    cursor, conn = createCursorConn()

    try:
        cursor.execute("""
            INSERT INTO Semester (semester_name)
            VALUES (?)
        """, (semester_name,))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error create sem: {e}")
    finally:
        conn.close()


def create_user_semester(username: str, semester_name: str):
    cursor, conn = createCursorConn()

    try:
        #retrieve user_id
        cursor.execute("""
            SELECT user_id FROM User
            WHERE username = ?
        """, (username,))
        user_result = cursor.fetchone()


        #retrieve semester_id
        cursor.execute("""
            SELECT semester_id FROM Semester
            WHERE semester_name = ?
        """, (semester_name,))
        semester_result = cursor.fetchone()


        if user_result == None or semester_result == None:
            raise ValueError("User or Semester not found.")
        

        user_id = user_result[0]
        semester_id = user_result[0]

        cursor.execute("""
            INSERT INTO User_Semester (user_id, semester_id)
            VALUES(?, ?)
        """, (user_id, semester_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error create user sem: {e}")
    except ValueError as ve:
        print(f"Value error: {ve}")
    finally:
        conn.close()
