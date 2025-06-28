from datetime import datetime
import json
import os

CONFIG_PATH = os.getcwd() + r"/config.json"
DEFAULT_CONFIG = {
    "API": {
        "api_id": 0,
        "api_hash": "",
        "phone": "+7",
        "username": ""
    },
    "SenderSS": {
        "key": "",
        "theme": "dark",
        "groupsID": [""],
        "messagelink": ""
    }
}

def create_config_if_not_exists():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        log(f"Создан новый конфиг: {CONFIG_PATH}")
    else:
        pass

def get_config():
    try:
        with open("config.json") as cfg:
            config = json.load(cfg)
            return config
    except FileExistsError:
        create_config_if_not_exists()
        log("Ошибка: config.json не найден.")
    except Exception as e: 
        log(f"logger err: {e}")


def gett():
    return datetime.now().strftime("%H:%M:%S")

def log(text):
    print(f"[LOG]: {gett()} {text}")