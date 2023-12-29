import filecmp
import shutil
import os
import sys
import __main__

from .nodes.constants import PROJECT_NAME
from .nodes.properties_loader import LoadProperties
from .nodes.llm.baidu_translator import BaiduTranslator
from .nodes.llm.youdao_ai import YoudaoTranslator
from .nodes.llm.openai_gpt import OpenaiGPT
from .nodes.llm.azure_gpt import AzureOpenaiGpt
from .nodes.llm.chatglm_gpt import ChatGLMGpt
from .nodes.factxApi.llm import FactxApiBaiduTranslator, FactxApiYoudaoTranslator, FactxAzureOpenaiGPT, FactxChatGlmGPT
from .nodes.tool.preview import ShowText,ShowWebImage
from .nodes.tool.number_input import IntNode,FloatNode,BooleanNode
from .nodes.tool.loader import ParamHub,StringHub9,VideoParamHub
from .nodes.tool.batch import ImageBatch9,LatentBatch9
from .nodes.tool.text import TextNode,ConcatText,ReplaceText,TrimText
from .nodes.image.image_mask import MaskInvert
from .nodes.image.image_process import WatermarkOffset,ImageScale_Side,CropImage

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
    FactxApiBaiduTranslator.NAME: FactxApiBaiduTranslator,
    FactxApiYoudaoTranslator.NAME: FactxApiYoudaoTranslator,
    FactxAzureOpenaiGPT.NAME: FactxAzureOpenaiGPT,
    FactxChatGlmGPT.NAME: FactxChatGlmGPT,

    ShowText.NAME: ShowText,
    ShowWebImage.NAME: ShowWebImage,
    MaskInvert.NAME: MaskInvert,
    WatermarkOffset.NAME: WatermarkOffset,
    ImageScale_Side.NAME: ImageScale_Side,
    CropImage.NAME: CropImage,

    IntNode.NAME: IntNode,
    FloatNode.NAME: FloatNode,
    BooleanNode.NAME: BooleanNode,
    TextNode.NAME: TextNode,
    ConcatText.NAME: ConcatText,
    ReplaceText.NAME: ReplaceText,
    TrimText.NAME: TrimText,
    ParamHub.NAME: ParamHub,
    VideoParamHub.NAME: VideoParamHub,
    StringHub9.NAME: StringHub9,
    ImageBatch9.NAME: ImageBatch9,
    LatentBatch9.NAME: LatentBatch9,

}

# display name
NODE_DISPLAY_NAME_MAPPINGS = {
    LoadProperties.NAME: "read properties 读取本地参数",
    OpenaiGPT.NAME: "OpenAI chatGPT",
    AzureOpenaiGpt.NAME: "Azure OpenAI GPT",
    ChatGLMGpt.NAME: "ChatGLM chatGPT 智谱AI",
    BaiduTranslator.NAME: "Baidu translator 百度翻译",
    YoudaoTranslator.NAME: "Youdao translator 有道翻译",
    FactxApiBaiduTranslator.NAME: "Baidu translator 百度翻译 (Factx API)",
    FactxApiYoudaoTranslator.NAME: "Youdao translator 有道翻译 (Factx API)",
    FactxAzureOpenaiGPT.NAME: "Azure OpenAI GPT (Factx API)",
    FactxChatGlmGPT.NAME: "ChatGLM chatGPT 智谱AI (Factx API)",

    ShowText.NAME: "show text 显示文字",
    ShowWebImage.NAME: "show web image 显示网图",
    MaskInvert.NAME: "Mask Invert 蒙版反转",
    WatermarkOffset.NAME: "calculate watermark offset 计算水印在主图上的坐标",
    ImageScale_Side.NAME: "upscale image to side 放大图片",
    CropImage.NAME: "crop image 剪裁图片",

    IntNode.NAME: "input or convert int 输入或转换整数",
    FloatNode.NAME: "input or convert float 输入或转换浮点数",
    BooleanNode.NAME: "input or convert boolean 输入或转换布尔值",
    TextNode.NAME: "text 输入文本",
    ConcatText.NAME: "concat text 合并文本",
    ReplaceText.NAME: "replace text 替换文本",
    TrimText.NAME: "trim text 消除文本前后空格",
    ParamHub.NAME: "parameter hub 参数集中输入框",
    StringHub9.NAME: "string hub 文本集中输入框",
    ImageBatch9.NAME: "image batch 图片批处理",
    LatentBatch9.NAME: "latent batch 潜空间批处理",
}

__all__ = [NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS]