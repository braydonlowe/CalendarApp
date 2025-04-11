from LearningSuite import learningSuite

from Shared import shared_imports
from sqLite import utils

def casAuthentication(debugMode: bool, username: str, password: str) -> bool:
    class_events = learningSuite.learningSuite(debugMode, username, password)
    return class_events #If we return class events, that means that we got in through cas


def loginFromCL(debugMode: bool, username: str, password: str) -> tuple[dict | None, bool | None]:
    user_exists, user_isValidated = utils.validate_user(username, password)
    #Just for debugging purposes:
    print(f"UserValidated: {user_isValidated}")

    if not user_exists:
        class_events = casAuthentication(debugMode, username, password)
        if class_events == None:
            print("User cannot be authenticated")
            return None, False
        print("User authenticated.")
        
        #Now we know if we have been authenticated
        canvas_url = input("Please enter your Canvas ICS URL: ")
        print(canvas_url)
        utils.create_user(username, password, canvas_url)
        
        #This will be removed later once we get multiple semesters possible
        utils.create_semester("Winter 2025")
        #create User_semester and associate them together
        utils.create_user_semester(username, "Winter 2025")
        #Associate/create class data and assignments data
        return class_events, True #The true here means that the user was authenticated through cas
    
    
    return None, user_isValidated