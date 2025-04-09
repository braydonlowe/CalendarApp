from LearningSuite import learningSuite
from Shared import shared_imports
from sqLite import utils

def casAuthentication(username: str, password: str) -> bool:
    return True


def loginFromCL():
    lines = shared_imports.sys.stdin.read().splitlines()

    username = lines[0]
    password = lines[1]

    user_isValidated = utils.validate_user(username, password)


    #Just for debugging purposes:
    print(f"UserValidated: {user_isValidated}")

    if not user_isValidated:
        authenticated = casAuthentication(username, password)
        if not authenticated:
            return