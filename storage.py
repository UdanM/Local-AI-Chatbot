import json


class ConversationStorage:

    def __init__(self, filename):
        self.filename = filename

    def save(self, messages):
        with open(self.filename, "w", encoding="utf-8") as file:  #opens the file for writing
            json.dump(messages, file, indent=4)

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:  #takes json from the file and converts it back to python data
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return []