import datetime
import os
import subprocess
import sys
import time, cv2
import platform
import fnc
from src.AI import prompts
from src import actions
from src.AI.BASE import Gen


if "gemini_api_key" not in os.listdir("src/AI/"):
    with open("src/AI/gemini_api_key", "w", encoding="utf-8") as f:
        f.write(input("[Gemini API Key] "))

ai = Gen()
ai.system_instructions = [
    {"text": prompts.Instructions.first_instruction},
    {"text": prompts.Instructions.action_instruction},
    {"text": prompts.Instructions.examples},
    {"text": prompts.Instructions.machine_info.format(**{"os": platform.system(),
                                                         "version": platform.release(),
                                                         "arch": platform.machine(),
                                                         "python": platform.python_version(),
                                                         "time": datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                                                         "cpu": platform.processor(),
                                                         "ram": actions.get_ram()})},]
ai.import_history_anyway("conversations/history")


msg = None

while True:
    if not msg:
        msg = f"{str(datetime.datetime.now())}\nfrom_user||"+input("[user] ")
    for keyword in ["||exit", "||выход"]:
        if keyword in msg:
            sys.exit(0)
    ai.history_add("user", msg)
    result = ai.generate()
    ai.history_add("assistant", result)
    try:
        target = result.split("||")[0]

        if target.lower() == "user":
            fnc.user_output(ai)
            msg = None
            time.sleep(1)

        elif target.lower() == "system":
            msg = fnc.system_output(ai)
            time.sleep(4)

    except Exception as e:
        print(e)
        msg = 'error||' + str(e)
        time.sleep(5)


