import json


def load_config():
    config = ""
    with open("config/config.json", "r") as conf:
        config = json.load(conf)

    conf.close()
    return config
