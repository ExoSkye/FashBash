import json
import os

def get_config(key):
    """
    Gets the key in the configuration file's value.
    """
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            json_obj = json.load(file)
            return json_obj[key]
    else:
        raise FileNotFoundError("config.json is missing!")

def set_config(key, value):
    """
    Sets a key in the configuration file to the value.
    """
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            json_obj = json.load(file)

        json_obj[key] = value

        with open("config.json", "w") as file:
            json.dump(json_obj, file)
    else:
        raise FileNotFoundError("config.json is missing!")

def create_config():
    """
    Creates a configuration file if it doesn't exist, then asking the user
    to supply the required values.
    """
    if os.path.exists("config.json"):
        return

    else:
        with open("config.json", "w") as file:
            print("Configuration file not found, creating a new one.")

            data = {
                "token": input("Discord bot token: "),
                "prefix": input("Discord bot prefix: "),
                "log_level": 20 # logging.INFO
            }

            json.dump(data, file, indent="    ")