import sys

from ..common import fields
from ..constants import get_project_name, get_project_category

NODE_CATEGORY = get_project_category("util/loader")


class ParamHub:
    NAME = get_project_name('ParamHub')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING", "STRING", "INT", "BOOLEAN", "STRING", "STRING",)
    RETURN_NAMES = ("prompt", "negativePrompt", "seed", "addWatermark", "watermark", "segment")
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": fields.STRING_ML,
                "negativePrompt": fields.STRING_ML,
                "seed": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": sys.maxsize,
                }),
                "addWatermark": fields.BOOL_TRUE,
                "watermark": fields.STRING,
                "segment": fields.STRING,
            }
        }

    def doWork(self, prompt, negativePrompt, seed, addWatermark, watermark, segment):
        if addWatermark==False:
            watermark = ''
        return {"result": (prompt, negativePrompt, seed, addWatermark, watermark, segment)}


class StringHub9:
    NAME = get_project_name('StringHub9')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("string1", "string2", "string3", "string4", "string5", "string6", "string7", "string8", "string9")
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string1": fields.STRING_ML,
                "string2": fields.STRING_ML,
                "string3": fields.STRING_ML,
                "string4": fields.STRING_ML,
                "string5": fields.STRING_ML,
                "string6": fields.STRING_ML,
                "string7": fields.STRING_ML,
                "string8": fields.STRING_ML,
                "string9": fields.STRING_ML,
                "base_string": fields.STRING_ML,
                "separator": ("STRING", {"multiline": False, "default": ","}),
                "concat": (["Before", "After", "None"],
                           {"default": "None"}),
            }
        }

    def doWork(self, string1, string2, string3, string4, string5, string6, string7, string8, string9, base_string,
               separator,
               concat):
        if concat == 'None':
            return {"result": (string1, string2, string3, string4, string5, string6, string7, string8, string9,)}
        elif concat == 'Before':
            return {"result": (
                string1 + separator + base_string, string2 + separator + base_string, string3 + separator + base_string,
                string4 + separator + base_string, string5 + separator + base_string, string6 + separator + base_string,
                string7 + separator + base_string, string8 + separator + base_string,
                string9 + separator + base_string,)}
        elif concat == 'After':
            return {"result": (
                base_string + separator + string1, base_string + separator + string2, base_string + separator + string3,
                base_string + separator + string4, base_string + separator + string5, base_string + separator + string6,
                base_string + separator + string7, base_string + separator + string8,
                base_string + separator + string9,)}
        else:
            pass
