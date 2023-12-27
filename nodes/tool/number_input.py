from ..constants import get_project_name, get_project_category

NODE_CATEGORY = get_project_category("util/number")

class Seed:
    NAME = get_project_name('Seed')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": 0xffffffffffffffff
                }),
            },
        }

    def doWork(self, int=0):
        return (int,)


class Int:
    NAME = get_project_name('Int')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
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
        return (int,)


class Float:
    NAME = get_project_name('Float')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)
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
        return (float,)


class FloatToInt:
    NAME = get_project_name('FloatToInt')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 0xffffffffffffffff, "forceInput": True}),
            }
        }

    def doWork(self, float):
        return (int(float),)


class IntToFloat:
    NAME = get_project_name('IntToFloat')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "int": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "forceInput": True}),
        }
        }

    def doWork(self, int):
        return (float(int),)


class IntToText:
    NAME = get_project_name('IntToText')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {"default": 0.0, "min": 0.0, "max": 0xffffffffffffffff, "forceInput": True}),
            }
        }

    def doWork(self, int):
        return (str(int),)


class FloatToText:
    NAME = get_project_name('FloatToText')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 0xffffffffffffffff, "forceInput": True}),
            }
        }

    def doWork(self, float):
        return (str(float),)
