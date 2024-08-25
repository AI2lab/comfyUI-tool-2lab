

from .constants import get_project_name, get_project_category, PROJECT_NAME

NODE_CATEGORY = get_project_category("util")

class Text:
    NAME = get_project_name('Text')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_NAMES = ("text", )
    RETURN_TYPES = ("STRING",)

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING", {"multiline": True, "default": ''}),
        },
    }

    def doWork(self, text=''):
        return {"ui": {"text": (text,)}, "result": (text,)}

class TextConcat:
    NAME = get_project_name('TextConcat')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text1": ("STRING", {"multiline": True, "default": ''}),
            "text2": ("STRING", {"multiline": True, "default": ''}),
            "text3": ("STRING", {"multiline": True, "default": ''}),
            "text4": ("STRING", {"multiline": True, "default": ''}),
            "delimiter": ("STRING", {"default": ",", "multiline": False}),
        },
    }

    def doWork(self, text1='', text2='', text3='', text4='', delimiter=''):
        text1 = '' if text1 == 'undefined' else text1
        text2 = '' if text2 == 'undefined' else text2
        text3 = '' if text3 == 'undefined' else text3
        text4 = '' if text4 == 'undefined' else text4

        if delimiter == '\\n':
            delimiter = '\n'

        concat = text1
        if(text2!=''):
            concat = concat+delimiter+text2
        if(text3!=''):
            concat = concat+delimiter+text3
        if(text4!=''):
            concat = concat+delimiter+text4
        return {"ui": {"text": (concat,)}, "result": (concat,)}

class ShowText:
    NAME = get_project_name('ShowText')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_NAMES = ("text", )
    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
          "required": {
            "text": ("STRING", {"forceInput":True}),
          },
        }

    def doWork(self, text=''):
        if text is None:
            text = ''
        value = text.strip()

        return {"ui": {"text": (value,)}, "result": (value,)}

NODE_CLASS_MAPPINGS = {
    Text.NAME: Text,
    TextConcat.NAME: TextConcat,

    ShowText.NAME: ShowText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    Text.NAME: "Text" + " (" + PROJECT_NAME + ")",
    TextConcat.NAME: "Text Concat" + " (" + PROJECT_NAME + ")",

    ShowText.NAME: "Show Text" + " (" + PROJECT_NAME + ")",
}