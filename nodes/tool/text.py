from ..constants import get_name,get_category

class Text:
    NAME = get_name('text')
    CATEGORY = get_category("util/text")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    def doWork(self, text):
        return (text+" ",)

class ConcatText:
    NAME = get_name('concat_text')
    CATEGORY = get_category("util/text")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "text1": ("STRING", {"multiline": True, "defaultBehavior": "input"}),
            "text2": ("STRING", {"multiline": True, "defaultBehavior": "input"}),
            "separator": ("STRING", {"multiline": False, "default": ","}),
        }}

    @ staticmethod
    def doWork(text1, separator, text2):
        return (text1 + separator + text2,)

class TrimText:
    NAME = get_name('trim_text')
    CATEGORY = get_category("util/text")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "text": ("STRING", {"multiline": False, "defaultBehavior": "input"}),
        }}

    def doWork(self, text):
        return (text.strip(),)

class ReplaceText:
    NAME = get_name('replace_text')
    CATEGORY = get_category("util/text")
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "text": ("STRING", {"multiline": True, "defaultBehavior": "input"}),
            "old": ("STRING", {"multiline": False}),
            "new": ("STRING", {"multiline": False})
        }}

    @ staticmethod
    def doWork(text, old, new):
        return (text.replace(old, new),)  # replace a text with another text