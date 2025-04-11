import sqlite3
from sqLite import create_tables
import bcrypt
from datetime import datetime, timedelta, date


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


def get_user_id(username: str) -> int:
    cursor, conn = createCursorConn()

    try:
        cursor.execute("""
            SELECT user_id FROM User
            WHERE username = ?
        """, (username,))
        user_result = cursor.fetchone()
        return user_result[0]
    except sqlite3.Error as e:
        print(f"Database error get user id: {e}")
    finally:
        conn.close()



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



#User_Semester
def create_user_semester(username: str, semester_name: str):
    cursor, conn = createCursorConn()

    try:
        #retrieve user_id
        cursor.execute("""
            SELECT user_id FROM User
            WHERE username = ?
        """, (username,))
        user_result = cursor.fetchone()


        if user_result == None:
            raise ValueError("User or Semester not found.")
        

        user_id = user_result[0]

        cursor.execute("""
            INSERT INTO User_Semester (user_id, semester_name)
            VALUES(?, ?)
        """, (user_id, semester_name))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error create user sem: {e}")
    except ValueError as ve:
        print(f"Value error: {ve}")
    finally:
        conn.close()


def get_semester_id(user_id: int, semester_name: str):
    cursor, conn = createCursorConn()

    try:
        cursor.execute("""
            SELECT semester_id FROM User_Semester
            WHERE user_id = ?
            AND semester_name = ?
        """, (user_id, semester_name))

        user_semester_result = cursor.fetchone()
        return user_semester_result[0]
    except sqlite3.Error as e:
        print(f"Database error get_semester_id: {e}")
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


def retrieve_classes(username: str):
    cursor, conn = createCursorConn()

    try:
        cursor.execute("""
            SELECT Class.class_name FROM User
            JOIN User_Semester ON User.user_id = User_Semester.user_id
            JOIN Class ON User_Semester.semester_id = Class.semester_id
            WHERE User.username = ?
        """, (username,))
        classes_result = cursor.fetchall()
        return [row[0] for row in classes_result]
    except sqlite3.Error as e:
        print(f"Database error retrieving canvas_url: {e}")
    finally:
        conn.close()


#For retrieving due date data
def get_one_week_dates() -> tuple[str, str]:
    today = date.today()

    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    string_monday = monday.strftime("%b %d")
    string_sunday = sunday.strftime("%b %d")

    return string_monday, string_sunday

def retrieve_due_all(username: str, semester_name):
    cursor, conn = createCursorConn()
    monday, sunday = get_one_week_dates()

    try:
        cursor.execute("""
            SELECT a.assignment_name, a.due_date, c.class_name
            FROM Assignments a
            JOIN Class c ON a.class_id = c.class_id
            JOIN User_Semester us ON us.semester_id = c.semester_id
            JOIN User u ON u.user_id = us.user_id
            WHERE u.username = ?
            AND us.semester_name = ?
            AND a.due_date BETWEEN ? AND ?
            AND a.completed = 0;
        """, (username, semester_name, monday, sunday))

        assignments = cursor.fetchall()
        return assignments

    except sqlite3.Error as e:
        print(f"Database error retrieving all assignments due: {e}")
    finally:
        conn.close()
    


def retrieve_due_class(username: str, semester_name: str, class_name: str):
    cursor, conn = createCursorConn()
    monday, sunday = get_one_week_dates()

    try:
        cursor.execute("""
            SELECT a.assignment_name, a.due_date, c.class_name
            FROM Assignments a
            JOIN Class c ON a.class_id = c.class_id
            JOIN User_Semester us ON us.semester_id = c.semester_id
            JOIN User u ON u.user_id = us.user_id
            WHERE u.username = ?
            AND us.semester_name = ?
            AND c.class_name = ?
            AND BETWEEN ? AND ?
            AND a.completed = 0
        """, (username, semester_name, class_name, monday, sunday))
    except sqlite3.Error as e:
        print(f"Database error retrieving class assignments due: {e}")
    finally:
        conn.close()
    