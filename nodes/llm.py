import hashlib
import json

from .caller import submit
from .constants import get_project_name, get_project_category, read_user_key,PROJECT_NAME

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
                "system_prompt": ("STRING", {"placeholder":"输入AI角色的描述","multiline": True}),
                "user_prompt": ("STRING", {"placeholder":"输入你的问题","multiline": True}),
                "max_tokens": ("INT", {"default": 512, "min": 100, "max": 1e5}),
                "temperature": ("FLOAT",{"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.01},),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def doWork(self,  system_prompt, user_prompt,max_tokens,temperature ,prompt=None, extra_pnginfo=None):
        command = "engine_llm_chat"

        userKey = read_user_key(prompt)
        # if userKey=='':
        #     raise Exception("请使用Input User Key节点，输入用户密钥")

        paramMap = {
            'userKey': userKey,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        responseJson = submit(command, json.dumps(paramMap))
        if responseJson['success']==True:
            result = responseJson['data']['result']
            result = result.strip()
            if result.startswith('"') and result.endswith('"'):
                result = result[1:-1].strip()
            return {"ui": {"text": (result,)}, "result": (result,)}
        else:
            result = responseJson['data']['result']
            return {"ui": {"text": (result,)}, "result": ('',)}

    @classmethod
    def IS_CHANGED(s, system_prompt, user_prompt,max_tokens,temperature ,prompt=None, extra_pnginfo=None):
        m = hashlib.sha256()
        m.update(system_prompt+'-'+user_prompt+'-'+str(max_tokens)+'-'+str(temperature))
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
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    def doWork(self,  to_lang, text,prompt=None, extra_pnginfo=None):
        command = "engine_llm_translate"

        # 读取 user key，从ini文件或者cookie中。如果读取失败，会弹出excepation
        userKey = read_user_key(prompt)
        # if userKey=='':
        #     raise Exception("请使用Input User Key节点，输入用户密钥")

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
    LLMChat.NAME: "LLM chat 大模型对话"+" ("+PROJECT_NAME+")",
    SimpleTranslator.NAME: "simple translator 简单翻译"+" ("+PROJECT_NAME+")",
}