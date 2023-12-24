import openai
from ..constants import get_name,get_category

class Openai_chatGPT:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "secret_key": ("KEY", {"multiline": False}),
                "prompt": ("STRING", {"multiline": True}),
                "model": (["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-vision-preview"],
                          {"default": "gpt-3.5-turbo"}),
            },
            "optional": {
                "image_url": ("TEXT", {"multiline": False}),
            }
        }

    NAME = get_name('Openai_chatGPT')
    CATEGORY = get_category("api")
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("text", "image_url")
    FUNCTION = "doWork"

    def doWork(self, secret_key, model, prompt, image_url=None):
        client = openai.OpenAI(
            api_key=secret_key
        )
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}]
        if image_url is not None:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": image_url,
                    },
                ], }
            ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            max_tokens=1000,
        )

        try:
            result = response.choices[0].message.content
            # print(result)
            return (result,)
        except:
            return ("openai api failed. openai api 调用失败",)
