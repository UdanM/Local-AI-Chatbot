import json


class Memory:

    def __init__(self, filename):
        self.filename = filename
        self.data = self.load()

    def load(self):

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def set(self, key, value):

        self.data[key] = value
        self.save()


    def get(self, key):

        return self.data.get(key)


    def clear(self):

        self.data = {}
        self.save()