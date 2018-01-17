import ujson as json

def load_config():
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
    else:
        return config
        
def save_config(config):
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(config))
    except OSError:
        print("Couldn't save /config.json")

