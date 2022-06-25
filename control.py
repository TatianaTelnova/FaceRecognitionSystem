import os

from class_storage_data import StorageData


def set_items_from_fit(collection, items):
    sd = StorageData(collection)
    sd.insert_all(items)


def set_items_from_widget(collection_path, items_save):
    collection_name = os.path.splitext(os.path.basename(collection_path))[0]
    sd = StorageData(collection_name)
    last_id = sd.count_save()
    for item in items_save:
        item["p_id"] = collection_name[0] + collection_name[1] + collection_name[2] + str(last_id)
        sd.insert_item(item)
        last_id += 1


def get_count_all(collection):
    sd = StorageData(collection)
    return sd.count_all()


def get_count_save():
    sd = StorageData()
    return sd.count_save()


def get_items_to_widget():
    sd = StorageData()
    return sd.select_save()


def delete_from_widget(collection_path):
    os.remove("resources/" + collection_path)
    collection = os.path.splitext(os.path.basename(collection_path))[0]
    sd = StorageData(collection)
    sd.delete_file()


def get_person_to_widget(collection, p_class):
    sd = StorageData(collection)
    items = sd.select_all()
    for item in items:
        if int(item["p_class"]) == p_class:
            return item["p_name"]
    return "unknown person"