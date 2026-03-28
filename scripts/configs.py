import json

def load_configs(config_path:str):
    return json.load(open(config_path))