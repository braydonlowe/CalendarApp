import sqlite3
from sqLite import create_tables
import bcrypt
from datetime import datetime


def createCursorConn() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    conn = sqlite3.connect("calendarApp.db")
    cursor = conn.cursor()
    return cursor, conn


#Get and create user
def validate_user(username: str, password: str) -> tuple[bool, bool]:
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
        return False, False #User exists, Password Match
    
    hashed_password = result[0]

    password_match = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return True, password_match



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



#Semester objects
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

def get_semester_id(semester_name: str) -> int | None:
    cursor, conn = createCursorConn()
    try:
        cursor.execute("""
            SELECT semester_id FROM Semester
            WHERE semester_name = ?
        """, (semester_name,))
        semester_result = cursor.fetchone()
        if semester_result:
            return semester_result[0]
        else:
            print("No semester id retrieved from the db.")
            return None
    except sqlite3.Error as e:
        print(f"Database error get sem ID: {e}")
    finally:
        conn.close()



#user semester
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



#These should be similar and should be executed in get schedule, and should also run in the ICS for canvas
def create_or_retrieve_class(semester_id: int, class_name: str)-> int | None:
    cursor, conn = createCursorConn()
    try:
        cursor.execute("""
            SELECT class_id FROM Class
            WHERE class_name = ?
            AND semester_id = ?
        """, (class_name, semester_id))
        class_retrieve = cursor.fetchone()

        if class_retrieve:
            return class_retrieve[0] #Will return the class_id

        #Create
        cursor.execute("""
            INSERT INTO Class (class_name, semester_id)
            VALUES(?, ?)
        """, (class_name, semester_id))
        conn.commit()

        return cursor.lastrowid

    except sqlite3.Error as e:
        print(f"Database error create or retrieve class: {e}")
        return None
    finally:
        conn.close()




def create_or_retrieve_assignment(class_id: int, assignment_name: str, due_date: str, completed: bool)-> int | None:
    #Format my due date into date time equivalent
    formatted_due_date = format_due_date(due_date)
    if not formatted_due_date:
        return None 
    

    cursor, conn = createCursorConn()
    try:
        cursor.execute("""
            SELECT assignment_id FROM Assignments
            WHERE assignment_name = ?
            AND class_id = ?
        """, (assignment_name, class_id))

        assignment_retrieve = cursor.fetchone()

        if assignment_retrieve:
            return assignment_retrieve[0] #Will return the assignment_id
        
        #Create
        cursor.execute("""
            INSERT INTO Assignments (assignment_name, class_id, due_date, completed)
            VALUES(?, ?, ?, ?)
        """, (assignment_name, class_id, due_date, completed))
        conn.commit()

        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error create or retrieve assignments: {e}")
        return None
    finally:
        conn.close()


def format_due_date(due_date_str: str) -> str:
    """
    Converts a date like 'Jan 11' to '2025-01-11' (assuming year 2025).
    """
    try:
        date_obj = datetime.strptime(due_date_str + " 2025", "%b %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError as e:
        print(f"Date formatting error: {e}")
        return None



def retrieve_ICS(username: str) -> str | None:
    cursor, conn = createCursorConn()
    try:
        cursor.execute("""
            SELECT canvas_url FROM User
            WHERE username = ?
        """, (username,))
        ics_result = cursor.fetchone()
        if ics_result:
            return ics_result[0]
        
        return None
    except sqlite3.Error as e:
        print(f"Database error retrieving canvas_url: {e}")
    finally:
        conn.close()
    

#Queries to run for the CL client.
