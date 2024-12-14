import datetime
import json
import os
import sys
import time
import platform
from src import fnc
from src.AI import prompts, actions
from src.AI.BASE import Gen


def main():
    # Create API key file if it doesn't exist
    if "gemini_api_key" not in os.listdir("src/AI/"):
        with open("src/AI/gemini_api_key", "w", encoding="utf-8") as f:
            f.write(input("[Gemini API Key] "))

    # Read settings.json file (jailbreak, temperature)
    settings = json.load(open("src/AI/settings.json", "r", encoding="utf-8"))

    # Create AI object
    ai = Gen()

    # Add system instructions
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
                                                             "ram": actions.get_ram()})}]

    # Import history
    if settings["jailbreak"]:

        # import jailbreak history
        ai.import_history_anyway("conversations/jailbreak_history")
    else:

        # import history
        ai.import_history_anyway("conversations/history")


    msg = None

    while True:
        # If no message from system - make user input
        # If message is "exit" or "выход" - exit.
        # Else - add to history and generate
        if not msg:
            msg = f"{str(datetime.datetime.now())}\nfrom_user||"+input("[user] ")
        for keyword in ["||exit", "||выход"]:
            if keyword in msg:
                sys.exit(0)
        ai.history_add("user", msg)
        result = ai.generate()
        ai.history_add("assistant", result)

        """If message is "user" - print user message.
           If message is "system" - print function then execute it. Send result to the history as "user"."""
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


if __name__ == "__main__":
    main()
