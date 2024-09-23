import json
import inspect

from .constants import get_project_name, get_project_category, PROJECT_NAME, AnyType

any = AnyType("*")

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
            "text2": ("STRING", {"multiline": True, "default": '',"lazy":True}),
            "text3": ("STRING", {"multiline": True, "default": '',"lazy":True}),
            "text4": ("STRING", {"multiline": True, "default": '',"lazy":True}),
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

class InsertText:
    NAME = get_project_name('InsertText')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "fullText": ("STRING", {"multiline": True, "default": ''}),
            "text1": ("STRING", {"forceInput": True, "default": ''}),
        },
        "optional":{
            "text2": ("STRING", {"forceInput": True, "default": ''}),
            "text3": ("STRING", {"forceInput": True, "default": ''}),
            "text4": ("STRING", {"forceInput": True, "default": ''}),
        }
    }

    def doWork(self,fullText='', text1='', text2='', text3='', text4=''):
        fullText = '' if fullText == 'undefined' else fullText
        text1 = '' if text1 == 'undefined' else text1
        text2 = '' if text2 == 'undefined' else text2
        text3 = '' if text3 == 'undefined' else text3
        text4 = '' if text4 == 'undefined' else text4

        concat = fullText.format(text1,text2,text3,text4)
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

class ShowAny:
    NAME = get_project_name('ShowAny')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_NAMES = ("text", )
    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
          "required": {
            "anything": (any, {}),
          },
        }

    def doWork(self, anything=None):
        value = ''
        if anything is not None:
            try:
                if type(anything) is str:
                    value = anything
                else:
                    val = json.dumps(anything)
                    value = str(val)
            except Exception:
                value = str(val)
                pass
        # print(f"ShowAny: {value}")
        return {"ui": {"text": (value,)}, "result": (value,)}

NODE_CLASS_MAPPINGS = {
    Text.NAME: Text,
    TextConcat.NAME: TextConcat,
    InsertText.NAME: InsertText,

    ShowText.NAME: ShowText,
    ShowAny.NAME: ShowAny,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    Text.NAME: "Text 固定文本" + " (" + PROJECT_NAME + ")",
    TextConcat.NAME: "Text Concat 拼接文本" + " (" + PROJECT_NAME + ")",
    InsertText.NAME: "Insert Text 插入文本" + " (" + PROJECT_NAME + ")",

    ShowText.NAME: "Show Text 显示文本" + " (" + PROJECT_NAME + ")",
    ShowAny.NAME: "Show Any 显示任意内容" + " (" + PROJECT_NAME + ")",
}