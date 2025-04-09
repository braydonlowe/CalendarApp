import sqlite3
from sqLite import create_tables
import bcrypt


def validate_user(username: str, password: str) -> bool:
    cursor, conn = create_tables.createCursorConn()

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

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
