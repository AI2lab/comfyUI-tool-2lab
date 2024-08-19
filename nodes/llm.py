import hashlib
import json

from .caller import submit
from .constants import get_project_name, get_project_category, read_user_key

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
                "system_prompt": ("STRING", {"multiline": True}),
                "user_prompt": ("STRING", {"multiline": True}),
            },
        }

    def doWork(self,  system_prompt, user_prompt):
        command = "engine_llm_chat"

        # 读取 user key，从ini文件或者cookie中。如果读取失败，会弹出excepation
        userKey = read_user_key()

        paramMap = {
            'userKey': userKey,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
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

class SimpleTranslator:
    NAME = get_project_name('SimpleTranslator')
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

        # 读取 user key，从ini文件或者cookie中。如果读取失败，会弹出excepation
        userKey = read_user_key()

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


NODE_CLASS_MAPPINGS = {
    LLMChat.NAME: LLMChat,
    SimpleTranslator.NAME: SimpleTranslator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    LLMChat.NAME: "LLM chat",
    SimpleTranslator.NAME: "simple translator",
}