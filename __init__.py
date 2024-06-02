import filecmp
import json
import shutil
import os
import sys
import __main__
import traceback

from .nodes.api.caller import submit
from .nodes.utils import create_qr_code, auto_download_model, print_console
from .nodes.constants import PROJECT_NAME, userKey_file, project_root, read_user_key, config_file, config_template_file, \
    config
from .nodes.api.llm import LLMChat,  Translator
from .nodes.pack.apiNodes import InputImage, InputSeed, InputText, InputChoice, OutputText, OutputImage, \
    PublishWorkflow, CheckpointLoader, LoraLoader, ControlNetLoader, VAELoader
python = sys.executable

print_console("[comfyUI-tool-2lab] start")

# User extension files in custom_nodes
project_name = PROJECT_NAME
extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                 "web" + os.sep + "extensions" + os.sep + project_name)
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

# 如果user key不存在，创建
if not os.path.exists(userKey_file):
    # allocate user key from server
    command = "engine_wx2lab_create_user_key"
    paramMap = {}
    responseJson = submit(command, json.dumps(paramMap))
    print(responseJson)
    if responseJson['success'] and responseJson['data']:
        userKey = responseJson['data']['userKey']
        # 覆盖userKey
        with open(userKey_file, 'w', encoding='utf-8') as file:
            file.write(userKey)
else:
    userKey = read_user_key()

# 如果QRcode不存在，创建
qr_file_path = os.path.join(project_root, "2lab_key.png")
if userKey is not None and not os.path.exists(qr_file_path):
    url = "https://www.2lab.cn/wx2lab/bind/" + userKey
    print("QR key not found. creating : ",url)
    create_qr_code(url, qr_file_path)


# 如果config中指定自动下载模型，则执行下载
if config['auto_download_model']:
    auto_download_model()

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    LLMChat.NAME: LLMChat,
    Translator.NAME: Translator,

    CheckpointLoader.NAME: CheckpointLoader,
    LoraLoader.NAME: LoraLoader,
    VAELoader.NAME: VAELoader,
    ControlNetLoader.NAME: ControlNetLoader,

    InputImage.NAME: InputImage,
    InputSeed.NAME: InputSeed,
    InputText.NAME: InputText,
    # InputChoice.NAME: InputChoice,
    OutputText.NAME: OutputText,
    OutputImage.NAME: OutputImage,
    PublishWorkflow.NAME: PublishWorkflow,

}

# display name
NODE_DISPLAY_NAME_MAPPINGS = {
    LLMChat.NAME: "LLM chat",
    Translator.NAME: "translator",

    CheckpointLoader.NAME: "load available checkpoint"+" ("+PROJECT_NAME+")",
    LoraLoader.NAME: "load available lora"+" ("+PROJECT_NAME+")",
    VAELoader.NAME: "load available vae"+" ("+PROJECT_NAME+")",
    ControlNetLoader.NAME: "load available controlnet"+" ("+PROJECT_NAME+")",

    InputSeed.NAME: "input seed"+" ("+PROJECT_NAME+")",
    InputImage.NAME: "input image"+" ("+PROJECT_NAME+")",
    InputText.NAME: "input Text"+" ("+PROJECT_NAME+")",
    # InputChoice.NAME: "input Choise"+" ("+PROJECT_NAME+")",
    OutputText.NAME: "output text"+" ("+PROJECT_NAME+")",
    OutputImage.NAME: "output image"+" ("+PROJECT_NAME+")",
    PublishWorkflow.NAME: "publish workflow to 2lab"+" ("+PROJECT_NAME+")",
}

__all__ = [NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS]

print_console("[comfyUI-tool-2lab] finished")