from ..constants import get_project_name,get_project_category

NODE_CATEGORY = get_project_category("util/text")

class TextNode:
    NAME = get_project_name('text')
    CATEGORY = NODE_CATEGORY
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
    NAME = get_project_name('concat_text')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "text1": ("STRING", {"multiline": True, "forceInput": True}),
            "text2": ("STRING", {"multiline": True, "forceInput": True}),
            "separator": ("STRING", {"multiline": False, "default": ","}),
        }}

    @ staticmethod
    def doWork(text1, separator, text2):
        return (text1 + separator + text2,)

class TrimText:
    NAME = get_project_name('trim_text')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "text": ("STRING", {"multiline": True, "forceInput": True}),
        }}

    def doWork(self, text):
        return (text.strip(),)

class ReplaceText:
    NAME = get_project_name('replace_text')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @ classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "text": ("STRING", {"multiline": True, "forceInput": True}),
            "old": ("STRING", {"multiline": False}),
            "new": ("STRING", {"multiline": False})
        }}

    @ staticmethod
    def doWork(text, old, new):
        return (text.replace(old, new),)  # replace a text with another text