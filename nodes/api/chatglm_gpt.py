
from ..constants import get_name,get_category

class ChatGLMGpt:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("KEY", {"multiline": False, "default": ""}),
                "prompt": ("STRING", {"multiline": True}),
                "model": (["chatglm_turbo",],
                          {"default": "chatglm_turbo"}),
            },
        }

    NAME = get_name('ChatGLM_GPT')
    CATEGORY = get_category("api")
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("text", )
    FUNCTION = "doWork"

    def doWork(self, api_key, model, prompt):

        # 要使用时才import
        import zhipuai
        zhipuai.api_key = api_key
        messages = [
            {"role": "user", "content": prompt}]
        response = zhipuai.model_api.invoke(
            model=model,
            prompt=messages,
            # prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )

        if response['code']==200:
            try:
                result = response['data']['choices'][0]['content']
                # print("result = ", result)
                return (result,)
            except:
                print ("chatGlm api failed. chatGlm api 调用失败",)
                pass
        return ("",)