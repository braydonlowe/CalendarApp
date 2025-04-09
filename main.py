from LearningSuite import learningSuite
from Canvas import getICS
from Shared import authentication
from Shared import shared_imports
from sqLite import create_tables
from sqLite import utils


def main():
    debugMode = False
    #If not in debug mode, we should have 3 inputs <program>,<username>,<password> these are piped in.
    number_args = len(shared_imports.sys.argv)
    if number_args >= 3 and number_args <= 4:
        if number_args == 4:
            if shared_imports.sys.argv[3] == "DEBUG":
                debugMode = True
            else:
                print("ERROR: Unknown command inputed after username and password.")
                return
        username = shared_imports.sys.argv[1]
        password = shared_imports.sys.argv[2]

    else:
        print("ERROR: Unknown inputs from the command line client. Please restart the program and try again.")
        return

    create_tables.createTables()
    authentication.loginFromCL(debugMode, username, password)
    #getICS.getICS()
    pass

if __name__ == "__main__":
    main()