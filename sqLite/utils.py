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
        print(f"Database error: {e}")
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

def create_semester():
    pass
