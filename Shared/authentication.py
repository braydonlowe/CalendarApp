import sqlite3
import pwinput
from LearningSuite import learningSuite

def casAuthentication(username: str, password: str) -> bool:
    pass

def getUser(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("")


def loginFromCL():
    print() #Just to create a line of spacing to make it look better
    username = input("Enter your NetID: ")
    password = pwinput.pwinput(prompt="Enter your password: ")

    user = getUser(username)

    if not user:
        authenticated = casAuthentication(username, password)