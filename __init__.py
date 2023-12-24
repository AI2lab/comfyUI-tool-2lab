import filecmp
import shutil
import os
import sys
import __main__
from .nodes.api.baidu_translator import baidu_translator
from .nodes.api.youdao_ai import youdao_translator
from .nodes.loader import LoadProperties
from .nodes.tool.previewNode import ShowText,ShowWebImage
from .nodes.api.openai_gpt import Openai_chatGPT
from .nodes.api.azure_gpt import Azure_openai_gpt
from .nodes.api.chatGlm import ChatGLM_GPT

python = sys.executable

# User extension files in custom_nodes
project_name = "2lab"
extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),"web" + os.sep + "extensions" + os.sep + project_name)
javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

if not os.path.exists(extentions_folder):
    os.mkdir(extentions_folder)

result = filecmp.dircmp(javascript_folder, extentions_folder)

if result.left_only or result.diff_files:
    file_list = list(result.left_only)
    file_list.extend(x for x in result.diff_files if x not in file_list)

    for file in file_list:
        src_file = os.path.join(javascript_folder, file)
        dst_file = os.path.join(extentions_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_file)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "properties_loader": LoadProperties,
    "Openai_chatGPT": Openai_chatGPT,
    "Azure_Openai_GPT": Azure_openai_gpt,
    "ChatGLM_GPT": ChatGLM_GPT,
    "baidu_translator": baidu_translator,
    "youdao_translator": youdao_translator,
    "show_text": ShowText,
    "show_web_image": ShowWebImage,
}

# display name
NODE_DISPLAY_NAME_MAPPINGS = {
    "properties_loader": "read properties 读取本地参数",
    "Openai_chatGPT": "OpenAI chatGPT",
    "Azure_Openai_GPT": "Azure OpenAI GPT",
    "ChatGLM_GPT": "ChatGLM chatGPT 智谱AI",
    "baidu_translator": "Baidu translator 百度翻译",
    "youdao_translator": "Youdao translator 有道翻译",
    "show_text": "show text 显示文字",
    "show_web_image": "show web image 显示网图",
}

__all__ = [NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS]