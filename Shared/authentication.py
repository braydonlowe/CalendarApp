import sqlite3
import pwinput
from LearningSuite import learningSuite
from Shared import shared_imports

def casAuthentication(username: str, password: str) -> bool:
    pass

def getUser(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("")


def loginFromCL():
    lines = shared_imports.sys.stdin.read().splitlines()

    username = lines[0]
    password = lines[1]

    user = getUser(username)

    #Just for debugging purposes:
    print(f"Username: {username}\n Password: {password}\n\n")

    if not user:
        authenticated = casAuthentication(username, password)