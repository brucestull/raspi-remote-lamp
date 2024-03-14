import json


def load_config(file_path):
    with open(file_path, "r") as f:
        config = json.load(f)
    return config


# Assuming you have a config.json file with your settings
config = load_config("config.json")

# Now you can access your configuration settings
print(config["env"])
print(config["ssid"])
print(config["password"])
print(config["lamp_host"])
