import requests
from Shared import getConfig


def getICS():
    config = getConfig.load_config()

    ics_url = config.get("ICS_Link")

    response = requests.get(ics_url)

    if response.status_code == 200:
        with open("calendar.ics", "wb") as file:
            file.write(response.content)
        print("Doenload successful!")

    else:
        print("Failed to download:", response.status_code)