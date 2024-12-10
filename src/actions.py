import datetime
import sys

from src.AI.BASE import Gen


def pick(filename, data):
    import pickle

    with open(filename, "wb") as f:
        pickle.dump(data, f)


def unpick(filename):
    import pickle

    with open(filename, "rb") as f:
        return pickle.load(f)


def get_time() -> str:
    import datetime
    return "from_system||"+str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y")})


def create_dir(name: str) -> str:
    import os, datetime

    try:
        os.mkdir(name)
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "name": name,
                                      "action": "create",
                                      "status": "ok"})
    except:
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "name": name,
                                      "action": "create",
                                      "status": "error",
                                      "error": "Directory already exists"})


def remove_dir(name: str) -> str:
    import os

    try:
        os.rmdir(name)
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "dir_name": name,
                                      "action": "remove",
                                      "status": "ok"})
    except:
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "dir_name": name,
                                      "action": "remove",
                                      "status": "error",
                                      "error": "Directory does not exist"})


def get_memories() -> str:
    import os

    if "memories" not in os.listdir():
        pick("memories", [])

    return "from_system||" + str({"memories": unpick("memories")})


def add_memory(text: str) -> str:
    import os
    try:
        if "memories" not in os.listdir():
            pick("memories", [])
        memories = unpick("memories")
        memories.append(text)
        pick("memories", memories)
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "memory": text,
                                      "action": "add",
                                      "status": "ok"})
    except Exception as e:
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "memory": text,
                                      "action": "add",
                                      "status": "error",
                                      "error": str(e)})


def update_api_key(ai : Gen, key: str) -> str:
    ai.API_KEY = key
    try:
        with open("src/AI/gemini_api_key", "w", encoding="utf-8") as f:
            f.write(key)
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "api_key": key,
                                      "action": "update",
                                      "status": "ok"})
    except Exception as e:
        return "from_system||" + str({"time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                      "api_key": key,
                                      "action": "update",
                                      "status": "error",
                                      "error": str(e)})


def get_ram() -> str:
    import sys, subprocess

    if "psutil" not in sys.modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])

    import psutil

    return "from_system||" + str({"ram": psutil.virtual_memory().percent})