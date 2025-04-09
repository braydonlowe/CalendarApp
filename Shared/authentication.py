from LearningSuite import learningSuite

from Shared import shared_imports
from sqLite import utils

def casAuthentication(debugMode: bool, username: str, password: str) -> bool:
    success = learningSuite.learningSuite(debugMode, username, password)
    return success


def loginFromCL(debugMode: bool, username: str, password: str):
    user_isValidated = utils.validate_user(username, password)
    #Just for debugging purposes:
    print(f"UserValidated: {user_isValidated}")

    if not user_isValidated:
        authenticated = casAuthentication(debugMode, username, password)
        print(f"Authenticated: {authenticated}")
        if authenticated:
            canvas_url = input("Please enter your Canvas ICS URL: ")
            print(canvas_url)
            utils.create_user(username, password, canvas_url)
            
            #This will be removed later once we get multiple semesters possible
            utils.create_semester("Winter 2025")
            #create User_semester and associate them together
            utils.create_user_semester(username, "Winter 2025")
            #Associate/create class data and assignments data
            return