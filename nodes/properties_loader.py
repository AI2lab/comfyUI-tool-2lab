import json
import os
from .constants import get_project_name, get_project_category, project_root

NODE_CATEGORY = get_project_category("")

class LoadProperties:
    key_dict = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": (cls.get_key_list(), {"default": ""}),
            },
        }

    NAME = get_project_name('properties_loader')
    CATEGORY = NODE_CATEGORY
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
                # print("config_path = ", config_path)
                with open(config_path, 'r') as f:
                    cls.key_dict = json.load(f)
            except:
                print("failed to load properties")
                pass
        return list(cls.key_dict.keys())
