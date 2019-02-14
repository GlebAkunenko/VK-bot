import json


class FileManager:

    @staticmethod
    def read_data_from_json(path):
        file = open(path, mode='r', encoding='utf-8')
        string = file.read()
        file.close()
        return json.loads(string)

    @staticmethod
    def write_data_to_json(path, data):
        file = open(path, mode='w', encoding='utf-8')
        string = json.dumps(data, sort_keys=True, indent=4)
        file.write(string)
        file.close()