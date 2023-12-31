import json
import os
from ..constants import get_project_name,get_project_category,project_root

root_path = project_root

NODE_CATEGORY = get_project_category("llm")

class AzureOpenaiGpt:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": ("KEY", {"multiline": False, "default": ""}),
                "endpoint": ("KEY", {"multiline": False, "default": ""}),
                "deployment": ("KEY", {"multiline": False, "default": ""}),
                "version": ("KEY", {"multiline": False, "default": ""}),
                "prompt": ("STRING", {"multiline": True}),
            }
        }

    NAME = get_project_name('Azure_Openai_GPT')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    def doWork(self, key,endpoint, deployment,version, prompt):
        print(prompt)
        print(deployment)

        # 要使用时才import
        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=key,
            api_version=version,
            azure_endpoint=endpoint
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": prompt}
            ],
            model=deployment,
            stream=False,
            max_tokens=1000,
        )

        try:
            result = response.choices[0].message.content
            # print(result)
            return (result,)
        except:
            return ("Azure openai api failed. Azure openai api 调用失败",)


    @classmethod
    def get_model_list(cls):
        if cls.deployments is None:
            try:
                config_path = os.path.join(root_path, 'properties.json')
                with open(config_path, 'r') as f:
                    key_dict = json.load(f)
                    cls.deployments = key_dict.get("azure_openai_deployment").split(',')
                    cls.versions = key_dict.get("azure_openai_version").split(',')
            except:
                print("failed to load deployments or versions")
                pass
        return cls.deployments
