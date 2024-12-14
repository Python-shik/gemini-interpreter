import os
import requests
import json
import argparse
from src.AI import prompts

arg_parser = argparse.ArgumentParser(description="GeminiInterpreter")
arg_parser.add_argument("--jailbreak", action="store_true", help="Jailbreak mode", default=False)
arg_parser.add_argument("--temperature", type=float, default=1.0, help="Temperature")


args = arg_parser.parse_args()
settings = json.load(open("src/AI/settings.json", "r", encoding="utf-8"))

for i in ["temperature", "jailbreak"]:
    settings[i] = args.__dict__[i]


with open("src/AI/settings.json", "w", encoding="utf-8") as f:
    json.dump(settings, f, indent=4)


class Gen:
    """
Основной класс для работы с моделью генерации текста Gemini от Google.
Перед использованием - переназначьте переменную Gen.API_KEY на свой ключ от GeminiAI.

    Attributes:
        history: Список словарей с историею диалога.
        system_instructions: Список словарей с инструкциями системы.
    Methods:
        history_add(role, content): Добавляет сообщение в историю диалога.
        generate(): Генерирует текст на основе истории диалога.
        export_history(filename): Сохраняет историю диалога в файл.
        import_history(filename): Загружает историю диалога из файла.
        clear_history(filename): Очищает историю диалога.
    """
    def __init__(self, history=[], system_instructions=None):
        """Инициализация класса.

        Args:
            history (list, optional): Список словарей с историей диалога. Defaults to [].
            system_instructions (list, optional): Список словарей с инструкциями системы. Defaults to None.
"""
        self.API_KEY = open("src/AI/gemini_api_key", "r", encoding="utf-8").read()
        self.history = history
        self.system_instructions = system_instructions

    def history_add(self, role, content):
        """
        Add a message to the conversation history.

        Args:
            role (str): Роль отправителя сообщения.
            content (str): Текст сообщения.

        Returns:
            None
        """
        self.history.append({"role": role, "parts": [{"text": content}]})

    def generate(self):
        settings = json.load(open("src/AI/settings.json", "r", encoding="utf-8"))

        """
Генерирует текст на основе истории диалога из переменной Gen.history.

        Returns:
            str: Генерированный текст.
        """
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.API_KEY}"

        data = {"contents": self.history}

        if self.system_instructions:
            data["systemInstruction"] = {"role": "user", "parts": self.system_instructions}
            if {"text": prompts.Instructions.jailbreak_instruction} not in self.system_instructions:
                if settings["jailbreak"]:
                    self.system_instructions.append({"text": prompts.Instructions.jailbreak_instruction})

        data["generationConfig"] = {
            "temperature": settings["temperature"]
        }

        if settings["jailbreak"] == True:
            data["safetySettings"] = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_NONE"}
            ]

        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            print(response.json())
        result = str(response.json()["candidates"][0]["content"]["parts"][0]["text"])

        return result

    def export_history(self, filename):
        """
        Сохраняет историю диалога в файл.

        Args:
            filename (str): Имя файла.

        Returns:
            None
        """
        import pickle

        with open(filename, "wb") as f:
            pickle.dump(self.history, f)

    def import_history(self, filename):
        """
        Загружает историю диалога из файла.

        Args:
            filename (str): Имя файла.

        Returns:
            None
        """
        import pickle

        with open(filename, "rb") as f:
            self.history = pickle.load(f)

    def import_history_anyway(self, filename):
        try:
            self.import_history(filename)
        except FileNotFoundError:
            self.export_history(filename)  # Сохранит пустой список, так как беседа не начата
            self.import_history_anyway(filename)

    def clear_history(self, filename):
        """
        Очищает историю диалога.

        Args:
            filename (str): Имя файла.

        Returns:
            None
        """
        os.remove(filename)
        self.history = []


