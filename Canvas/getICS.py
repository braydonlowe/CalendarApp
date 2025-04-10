import requests
import re
from sqLite import utils
from ics import Calendar


def parseICS() -> dict:
    scheduledItems = {}  # Dictionary to hold the assignments grouped by class name
    
    try:
        # Open and read the .ics file
        with open("calendar.ics", "r", encoding="utf-8") as file:
            calendar = Calendar(file.read())
        
        # Parse each event and extract details
        for event in calendar.events:
            # Extract class name using regex from the SUMMARY field
            match = re.search(r'\[(.*?)\]', event.name)  # Looks for text inside the brackets
            class_name = match.group(1) if match else "Unknown Class"  # Default to "Unknown Class" if no match
            
            assignment_details = {
                "assignment": event.name,
                "due_date": event.begin.strftime("%b %d"),
                "completed": False  # Assuming not completed by default, you can change this based on your needs
            }

            # If the class_name is not yet in scheduledItems, add it
            if class_name not in scheduledItems:
                scheduledItems[class_name] = []
            
            # Append the assignment to the corresponding class name
            scheduledItems[class_name].append(assignment_details)
        
        return scheduledItems

    except FileNotFoundError:
        print("ICS file not found.")
        return {}

    except Exception as e:
        print(f"Error parsing ICS file: {e}")
        return {}





def getICS(username: str) -> None:
    #We are going to retrieve the ICS link from our DB.
    ics_url = utils.retrieve_ICS(username)

    if ics_url == None:
        print("There is no ICS URL. Sorry, that's unfortunate.")
        return
    response = requests.get(ics_url)

    if response.status_code == 200:
        with open("calendar.ics", "wb") as file:
            file.write(response.content)
        print("Download successful!")

    else:
        print("Failed to download:", response.status_code)


    return parseICS()