import filecmp
import shutil
import os
import sys
import __main__

from .nodes.constants import PROJECT_NAME
from .nodes.api.baidu_translator import BaiduTranslator
from .nodes.api.youdao_ai import YoudaoTranslator
from .nodes.api.properties_loader import LoadProperties
from .nodes.tool.preview import ShowText,ShowWebImage
from .nodes.tool.number_input import Int,Float,FloatToInt,IntToFloat,IntToText,FloatToText,Seed
from .nodes.tool.text import Text,ConcatText,ReplaceText,TrimText
from .nodes.api.openai_gpt import OpenaiGPT
from .nodes.api.azure_gpt import AzureOpenaiGpt
from .nodes.api.chatglm_gpt import ChatGLMGpt
from .nodes.image.image_mask import MaskInvert
from .nodes.image.txt_to_image import Txt2Img,Txt2ImgMultiline

python = sys.executable

# User extension files in custom_nodes
project_name = PROJECT_NAME
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
    LoadProperties.NAME: LoadProperties,
    OpenaiGPT.NAME: OpenaiGPT,
    AzureOpenaiGpt.NAME: AzureOpenaiGpt,
    ChatGLMGpt.NAME: ChatGLMGpt,
    BaiduTranslator.NAME: BaiduTranslator,
    YoudaoTranslator.NAME: YoudaoTranslator,
    ShowText.NAME: ShowText,
    ShowWebImage.NAME: ShowWebImage,
    MaskInvert.NAME: MaskInvert,
    Txt2Img.NAME: Txt2Img,
    Txt2ImgMultiline.NAME: Txt2ImgMultiline,
    Int.NAME: Int,
    Float.NAME: Float,
    IntToText.NAME: IntToText,
    FloatToText.NAME: FloatToText,
    IntToFloat.NAME: IntToFloat,
    FloatToInt.NAME: FloatToInt,
    Seed.NAME: Seed,
    Text.NAME: Text,
    ConcatText.NAME: ConcatText,
    ReplaceText.NAME: ReplaceText,
    TrimText.NAME: TrimText,
}

# display name
NODE_DISPLAY_NAME_MAPPINGS = {
    LoadProperties.NAME: "read properties 读取本地参数",
    OpenaiGPT.NAME: "OpenAI chatGPT",
    AzureOpenaiGpt.NAME: "Azure OpenAI GPT",
    ChatGLMGpt.NAME: "ChatGLM chatGPT 智谱AI",
    BaiduTranslator.NAME: "Baidu translator 百度翻译",
    YoudaoTranslator.NAME: "Youdao translator 有道翻译",
    ShowText.NAME: "show text 显示文字",
    ShowWebImage.NAME: "show web image 显示网图",
    MaskInvert.NAME: "Mask Invert 蒙版反转",
    Txt2Img.NAME: "text to image 文字转图片",
    Txt2ImgMultiline.NAME: "multiline text to image 多行文字转图片",
    Int.NAME: "input int 输入整数",
    Float.NAME: "input float 输入浮点数",
    IntToText.NAME: "input to text 整数变成字符串",
    FloatToText.NAME: "float to text 浮点数变成字符串",
    IntToFloat.NAME: "int to float 整数变成浮点数",
    FloatToInt.NAME: "float to int 浮点数变成整数",
    Seed.NAME: "seed 输入种子",
    Text.NAME: "text 输入文本",
    ConcatText.NAME: "concat text 合并文本",
    ReplaceText.NAME: "replace text 替换文本",
    TrimText.NAME: "trim text 消除文本前后空格",
}

__all__ = [NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS]