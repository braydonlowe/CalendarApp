from LearningSuite import learningSuite
from Canvas import getICS
import sys


def main():
    debugMode = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "DEBUG":
            debugMode = True
        else:
            print("ERROR: Unknown Command. Exiting process.")

    learningSuite.learningSuite(debugMode)
    getICS.getICS()
    pass

if __name__ == "__main__":
    main()