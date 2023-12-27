import json
import requests
from ..constants import get_project_name,get_project_category

api_server_url = "http://api.factx.cn/api/v4";

NODE_CATEGORY = get_project_category("factxApi/llm")

class FactxResponse:
    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data = data

def submit(command: str, data: str) -> FactxResponse:
    print(command)
    print(data)

    submitUrl = (api_server_url + "/i?c={}").format(command);
    headers = {
        'content-type': 'application/json;charset=utf-8',
    }
    response = requests.post(submitUrl, headers=headers, data=data)
    print(response.text)

    factxResponse = json.loads(response.text)
    print(factxResponse)
    return factxResponse

class FactxApiBaiduTranslator:
    NAME = get_project_name('factx_api_baidu_translator')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_id": ("KEY", {"forceInput": True}),
                "api_key": ("KEY", {"forceInput": True}),
                "text": ("STRING", {"multiline": True}),
                "to_lang": (["en", "zh"], {"default": "en"}),
            },
        }

    def doWork(self, api_id, api_key, to_lang, text):
        command = "app_factxApi_baidu_translator"
        paramMap = {
            "api_id": api_id,
            "api_key": api_key,
            "to_lang": to_lang,
            "text": text
        }
        responseJson = submit(command, json.dumps(paramMap))
        if responseJson['success']==True:
            translate_result = responseJson['data']['result']
            return {"result": (translate_result,)}
        else:
            return {"result": (responseJson['message'],)}

class FactxApiYoudaoTranslator:
    NAME = get_project_name('factx_api_youdao_translator')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "app_key": ("KEY", {"forceInput": True}),
                "app_secret": ("KEY", {"forceInput": True}),
                "text": ("STRING", {"multiline": True}),
                "to_lang": (["en", "zh-CHS"], {"default": "en"}),
            },
        }

    def doWork(self, app_key,app_secret, to_lang, text):
        command = "app_factxApi_youdao_translator"
        paramMap = {
            "app_key": app_key,
            "app_secret": app_secret,
            "to_lang": to_lang,
            "text": text
        }
        responseJson = submit(command, json.dumps(paramMap))
        if responseJson['success']==True:
            translate_result = responseJson['data']['result']
            return {"result": (translate_result,)}
        else:
            return {"result": (responseJson['message'],)}
