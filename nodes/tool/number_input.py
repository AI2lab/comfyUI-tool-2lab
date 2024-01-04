from ..common import fields
from ..constants import get_project_name, get_project_category

NODE_CATEGORY = get_project_category("util/number")

class BooleanNode:
    NAME = get_project_name('BooleanNode')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("Boolean","STRING",)
    RETURN_NAMES = ("boolean","string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "boolean": fields.BOOL_FALSE,
            },
        }

    def doWork(self, boolean=False):
        return (boolean,str(boolean),)

class IntNode:
    NAME = get_project_name('IntNode')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("INT","FLOAT","STRING",)
    RETURN_NAMES = ("int","float","string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {
                    "default": 0,
                    "min": -0xffffffffffffffff,
                    "max": 0xffffffffffffffff
                }),
            },
        }

    def doWork(self, int=0):
        return (int,float(int),str(int),)


class FloatNode:
    NAME = get_project_name('FloatNode')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("INT","FLOAT","STRING",)
    RETURN_NAMES = ("int","float","string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float": ("FLOAT", {
                    "default": 0,
                    "min": -0xffffffffffffffff,
                    "max": 0xffffffffffffffff
                }),
            },
        }

    def doWork(self, float=0):
        return (float,int(float),str(float),)
