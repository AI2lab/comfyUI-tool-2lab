
import json
import requests

api_server_url = "http://api.factx.cn/api/v4";

class FactxResponse:
    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data = data

def submit(command: str, data: str) -> FactxResponse:
    submitUrl = (api_server_url + "/i?c={}").format(command);
    headers = {
        'content-type': 'application/json;charset=utf-8',
    }
    try:
        response = requests.post(submitUrl, headers=headers, data=data)
        # print(response.text)

        factxResponse = json.loads(response.text)
        # print(factxResponse)
        return factxResponse
    except:
        print("call api failed")
        raise Exception("调用api接口失败 : ",submitUrl)
