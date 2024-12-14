import sys, pickle
import time, json, os, subprocess
import datetime
from src.AI.BASE import Gen, settings
from src.AI import actions


def user_output(ai):
    result = ai.history[-1]["parts"][0]["text"]
    to_print = result.split("||")[1]

    to_print = to_print.replace("**", "")

    print("[assistant] " + to_print)

    if settings["jailbreak"]:
        ai.export_history("conversations/jailbreak_history")
    else:
        ai.export_history("conversations/history")


def system_output(ai: Gen) -> str:
    result = ai.history[-1]["parts"][0]["text"]
    title = result.split("||")[1]
    exec_lang = result.split("||")[2]
    func4exec = result.split("||")[3]

    print(f"[assistant]", title)

    func4exec = func4exec.replace("```python", "")
    func4exec = func4exec.replace("```bash", "")
    func4exec = func4exec.replace("```cmd", "")
    func4exec = func4exec.replace("```", "")
    if exec_lang == "python":
        exec(func4exec)
        result = eval("f4exec()")

    msg = f"from_system||{result}"

    if "api_key" in eval(result).keys():
        ai.API_KEY = eval(result)["api_key"]

    return msg



