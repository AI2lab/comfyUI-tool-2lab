import json
import requests
from nodes.constants import get_name,get_category

api_server_url = "http://api.factx.cn/api/v4";

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

class CreateUser:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
        }

    NAME = get_name('factx_api_create_user')
    CATEGORY = get_category("api/factx")
    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("api_id","api_key","message",)
    FUNCTION = "doWork"
    CATEGORY = "🦊2lab/api/factx"

    def doWork(self):
        paramMap = {}
        command = "app_factxApi_create_user"
        response = submit(command,json.dumps(paramMap))
        print(response)
        if response['success']:
            resultJson = json.loads(response['data'])
            return {"result": (resultJson['api_id'],resultJson['api_key'],"create new user successfully",)}
        else:
            return {"result": ("","","create user failed",)}
