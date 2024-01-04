import sys

from ..common import fields
from ..constants import get_project_name, get_project_category

NODE_CATEGORY = get_project_category("util/loader")


class VideoParamHub:
    NAME = get_project_name('VideoParamHub')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ( "INT", "INT",)
    RETURN_NAMES = ("frames", "fps",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ([14,25], {"default": 14,}),
                "fps": ("INT", {"default": 5,
                       "min": 1,
                       "max": 1000,
                       "step": 1}),
            }
        }

    def doWork(self, frames, fps):
        return {"result": (frames, fps)}

class ParamHub:
    NAME = get_project_name('ParamHub')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING", "STRING", "INT", "INT", "INT", "INT", "BOOLEAN", "STRING", "STRING", "INT",)
    RETURN_NAMES = (
    "prompt", "negativePrompt", "width", "height", "seed", "steps", "addWatermark", "watermark", "segment", "batchSize")
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": fields.STRING_ML,
                "negativePrompt": fields.STRING_ML,
                "width": ("INT", {"default": 1024,
                       "min": 256,
                       "max": 2048,
                       "step": 1}),
                "height": ("INT", {"default": 1024,
                       "min": 256,
                       "max": 2048,
                       "step": 1}),
                "seed": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": sys.maxsize,
                }),
                "steps": ("INT", {"default": 25,
                       "min": 1,
                       "max": 1000,
                       "step": 1}),
                "addWatermark": fields.BOOL_TRUE,
                "watermark": fields.STRING,
                "segment": fields.STRING,
                "batchSize": fields.INT_POSITIVE,
            }
        }

    def doWork(self, prompt, negativePrompt, width, height, seed, steps, addWatermark, watermark, segment, batchSize):
        if addWatermark == False:
            watermark = ''
        return {"result": (prompt, negativePrompt, width, height, seed, steps, addWatermark, watermark, segment, batchSize)}

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
