import os
import json


class Storage:

    file_dir = ".storage"

    def __init__(self, name):
        self.name = name
        self.file_path = f"{self.file_dir}/{self.name}.json"
        self._check_storage()

    def _check_storage(self):
        if not os.path.isdir(self.file_dir):
            os.mkdir(self.file_dir)
        if not os.path.exists(self.file_path):
            open(self.file_path, "a").close()

    def get_dict(self):
        try:
            with open(self.file_path, "r") as json_file:
                return json.loads(json_file.read())
        except json.JSONDecodeError:
            return {}

    def update_storage(self, updated_dict: dict):
        with open(self.file_path, "w") as json_file:
            json_file.write(json.dumps(updated_dict))
