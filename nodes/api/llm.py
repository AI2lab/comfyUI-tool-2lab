import hashlib
import json

from .caller import submit
from ..constants import get_project_name, get_project_category, read_user_key

NODE_CATEGORY = get_project_category("llm")

class LLMChat:
    NAME = get_project_name('LLMChat')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
        }

    def doWork(self,  prompt):
        command = "engine_llm_chat"
        userKey = read_user_key()
        if userKey == "":
            raise Exception("还没设置userKey")
        paramMap = {
            'userKey': userKey,
            "prompt": prompt,
        }
        responseJson = submit(command, json.dumps(paramMap))
        if responseJson['success']==True:
            result = responseJson['data']['result']
            result = result.strip()
            if result.startswith('"') and result.endswith('"'):
                result =  result[1:-1].strip()
            return {"result": (result,)}
        else:
            return {"result": (responseJson['message'],)}

    @classmethod
    def IS_CHANGED(s, prompt):
        m = hashlib.sha256()
        m.update(prompt)
        return m.digest().hex()


class Translator:
    NAME = get_project_name('Translator')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "to_lang": (["en", "zh"], {"default": "en"}),
            },
        }

    def doWork(self,  to_lang, text):
        command = "engine_llm_translate"
        userKey = read_user_key()
        if userKey == "":
            raise Exception("还没设置userKey")
        paramMap = {
            'userKey': userKey,
            "to_lang": to_lang,
            "prompt": text
        }
        responseJson = submit(command, json.dumps(paramMap))
        if responseJson['success']==True:
            translate_result = responseJson['data']['result']
            return {"result": (translate_result,)}
        else:
            return {"result": (responseJson['message'],)}

    @classmethod
    def IS_CHANGED(s, to_lang, text):
        m = hashlib.sha256()
        m.update(to_lang+text)
        return m.digest().hex()
