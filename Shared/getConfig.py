import os
import json

BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Allows us to go up one level
CONFIG_PATH = os.path.join(BASE_DIRECTORY, "config.json")

"""
Loads the config.json into the specified folder.
"""
def load_config() -> dict:
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)