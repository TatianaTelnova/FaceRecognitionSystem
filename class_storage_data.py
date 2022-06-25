import os
import json


class StorageData(object):
    """
    StorageData класс добавляет данные в .json файлы
    """

    def __init__(self, collection_name=""):
        self.data = "data"
        self.collection = collection_name
        self.collection_save = "recognition_save"

    def check_folder(self):
        if not os.path.exists("resources/" + self.data):
            os.mkdir("resources/" + self.data)

    def check_file_all(self):
        if not os.path.exists("resources/" + self.data + "/" + self.collection + ".json"):
            with open("resources/" + self.data + "/" + self.collection + ".json", "w") as file:
                file.write("[]")

    def check_file_save(self):
        if not os.path.exists("resources/" + self.data + "/" + self.collection_save + ".json"):
            with open("resources/" + self.data + "/" + self.collection_save + ".json", "w") as file:
                file.write("[]")

    def delete_file(self):
        if os.path.exists("resources/" + self.data):
            if os.path.exists("resources/" + self.data + "/" + self.collection + ".json"):
                os.remove("resources/" + self.data + "/" + self.collection + ".json")

    def insert_all(self, items):
        self.check_folder()
        with open("resources/" + self.data + "/" + self.collection + ".json", "w", encoding="utf-8") as file:
            json.dump(items, file)

    def insert_item(self, item):
        self.check_folder()
        self.check_file_save()
        with open("resources/" + self.data + "/" + self.collection_save + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
        data.append(item)
        with open("resources/" + self.data + "/" + self.collection_save + ".json", "w", encoding="utf-8") as file:
            json.dump(data, file)

    def count_all(self):
        self.check_folder()
        self.check_file_all()
        with open("resources/" + self.data + "/" + self.collection + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return len(data)

    def count_save(self):
        self.check_folder()
        self.check_file_save()
        with open("resources/" + self.data + "/" + self.collection_save + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return len(data)

    def select_all(self):
        self.check_folder()
        self.check_file_all()
        with open("resources/" + self.data + "/" + self.collection + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def select_save(self):
        self.check_folder()
        self.check_file_save()
        with open("resources/" + self.data + "/" + self.collection_save + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data