import json
import os
from pathlib import Path
from ..constants import get_name, get_category, project_root

# cur_path = Path(__file__)
# root_path = cur_path.parent.parent.parent
# root_path = project_root
# print("root_path = ",root_path)

class LoadProperties:
    key_dict = None

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": (cls.get_key_list(), {"default": ""}),
            },
        }

    NAME = get_name('properties_loader')
    CATEGORY = get_category("api")
    RETURN_TYPES = ("KEY",)
    RETURN_NAMES = ("key",)
    FUNCTION = "doWork"

    def doWork(self, key):
        value = LoadProperties.key_dict.get(key)
        return {"result": (value,)}

    @classmethod
    def get_key_list(cls):
        if cls.key_dict is None:
            try:
                config_path = os.path.join(project_root, 'properties.json')
                print("config_path = ",config_path)
                with open(config_path, 'r') as f:
                    cls.key_dict = json.load(f)
            except:
                print("failed to load properties")
                pass
        return list(cls.key_dict.keys())

