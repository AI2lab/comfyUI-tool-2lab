import json
from comfy.model_management import InterruptProcessingException
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

class TextListConcatenate:
    NAME = get_project_name('TextListConcatenate')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_TYPES = ("LIST",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
            },
            "optional": {
                "list_1": ("LIST", {"forceInput": True}),
                "list_2": ("LIST", {"forceInput": True}),
                "list_3": ("LIST", {"forceInput": True}),
                "list_4": ("LIST", {"forceInput": True}),
            }
        }

    def doWork(self, **kwargs):
        concatenated_list: list[str] = []

        for k in sorted(kwargs.keys()):
            v = kwargs[k]

            # Only process "list" input ports.
            if isinstance(v, list):
                concatenated_list += v

        return (concatenated_list,)

class Text2List:
    NAME = get_project_name('Text2List')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_TYPES = ("LIST",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
            },
            "optional": {
                "text_1": ("STRING", {"forceInput": True}),
                "text_2": ("STRING", {"forceInput": True}),
                "text_3": ("STRING", {"forceInput": True}),
                "text_4": ("STRING", {"forceInput": True}),
            }
        }

    def doWork(self, **kwargs):
        concatenated_list: list[str] = []

        for k in sorted(kwargs.keys()):
            v = kwargs[k]

            if isinstance(v, str):
                concatenated_list.append(v)

        return (concatenated_list,)

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


class SaveText:
    NAME = get_project_name('SaveText')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_NAMES = ()
    RETURN_TYPES = ()
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
          "required": {
            "text": ("STRING", {"forceInput":True}),
            "path": ("STRING", {"default":''}),
          },
            "optional":{
                "filename": ("STRING", {"forceInput":True}),
            }
        }

    def doWork(self, text,path,filename=''):
        if text is None:
            text = ''
        text_to_save = text.strip()
        if path is None:
            raise ValueError(f"path can't be None")
        if filename:
            filepath = path.format(filename)
        else:
            filepath = path
        with open(filepath, 'w', encoding='utf-8') as file:
            # 将文本写入文件
            file.write(text_to_save)

class StopQueue:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "stop": ("BOOLEAN", {"forceInput": True}),
            },
        }

    NAME = get_project_name('StopQueue')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ()
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    def doWork(self,stop):
        if stop:
            raise InterruptProcessingException()
        return {}

NODE_CLASS_MAPPINGS = {
    Text.NAME: Text,
    TextConcat.NAME: TextConcat,
    InsertText.NAME: InsertText,
    TextListConcatenate.NAME: TextListConcatenate,
    Text2List.NAME: Text2List,

    ShowText.NAME: ShowText,
    SaveText.NAME: SaveText,
    # ShowAny.NAME: ShowAny,

    StopQueue.NAME: StopQueue,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    Text.NAME: "Text 固定文本" + " (" + PROJECT_NAME + ")",
    TextConcat.NAME: "Text Concat 拼接文本" + " (" + PROJECT_NAME + ")",
    InsertText.NAME: "Insert Text 插入文本" + " (" + PROJECT_NAME + ")",
    TextListConcatenate.NAME: "List Concatenate 多个列表合成列表" + " (" + PROJECT_NAME + ")",
    Text2List.NAME: "Text To List 多个文本合成列表" + " (" + PROJECT_NAME + ")",

    ShowText.NAME: "Show Text 显示文本" + " (" + PROJECT_NAME + ")",
    SaveText.NAME: "Save Text 保存文本" + " (" + PROJECT_NAME + ")",
    # ShowAny.NAME: "Show Any 显示任意内容" + " (" + PROJECT_NAME + ")",

    StopQueue.NAME: "stop queue 停止绘图" + " (" + PROJECT_NAME + ")",
}