from LearningSuite import learningSuite
from Canvas import getICS
from Shared import authentication
from Shared import shared_imports
from sqLite import create_tables
from sqLite import import_data
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
    class_events, authenticated = authentication.loginFromCL(debugMode, username, password)

    #If the user isn't valid we can just end the program.
    if not authenticated:
        return

    #If class events is none, it means either error or it already exists.
    if class_events != None:
        import_data.import_data_into_db(username, class_events)

    #canvas portion of the application
    canvas_class_events = getICS.getICS(username)

    if canvas_class_events != None:
        import_data.import_data_into_db(username, canvas_class_events)

   

    program_running = True
    while program_running:
        print("[1] SEE CLASSES")
        print("[2] DUE THIS WEEK")
        print("[3] QUIT")
        choice = input("Enter Input: ")
        if choice.isdecimal():
            number = int(choice)
            if number == 1:
                class_names = utils.retrieve_classes(username)
                for name in class_names:
                    print(name)
            elif number == 2:
                #Here is the call for everything due this week.
                assignments_this_week = utils.retrieve_due_all(username, "Winter 2025")
                print("Assignemnts due this week:\n")
                print(assignments_this_week)
                pass
            elif number == 3:
                return
            else:
                print("Please enter a number 1-3\n")
        else:
            print("Please enter a number 1-3\n")

if __name__ == "__main__":
    main()