from ..constants import get_name, get_category


class Seed:
    NAME = get_name('Int')
    CATEGORY = get_category("util/number")
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
    NAME = get_name('Int')
    CATEGORY = get_category("util/number")
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
    NAME = get_name('Float')
    CATEGORY = get_category("util/number")
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
    NAME = get_name('FloatToInt')
    CATEGORY = get_category("util/number")
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 0xffffffffffffffff, "defaultBehavior": "input"}),
            }
        }

    def doWork(self, float):
        return (int(float),)


class IntToFloat:
    NAME = get_name('IntToFloat')
    CATEGORY = get_category("util/number")
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "int": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "defaultBehavior": "input"}),
        }
        }

    def doWork(self, int):
        return (float(int),)


class IntToText:
    NAME = get_name('IntToText')
    CATEGORY = get_category("util/number")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {"default": 0.0, "min": 0.0, "max": 0xffffffffffffffff, "defaultBehavior": "input"}),
            }
        }

    def doWork(self, int):
        return (str(int),)


class FloatToText:
    NAME = get_name('FloatToText')
    CATEGORY = get_category("util/number")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 0xffffffffffffffff, "defaultBehavior": "input"}),
            }
        }

    def doWork(self, float):
        return (str(float),)
