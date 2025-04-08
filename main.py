from LearningSuite import learningSuite
from Canvas import getICS
from Shared import authentication
from Shared import shared_imports


def main():
    debugMode = False
    if len(shared_imports.sys.argv) > 1:
        if shared_imports.syssys.argv[1] == "DEBUG":
            debugMode = True
        else:
            print("ERROR: Unknown Command. Exiting process.")

    

    #learningSuite.learningSuite(debugMode)
    authentication.loginFromCL()
    getICS.getICS()
    pass

if __name__ == "__main__":
    main()