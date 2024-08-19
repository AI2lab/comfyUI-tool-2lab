import configparser
import json
import os
import traceback

import requests
import server
from aiohttp import web
from pathlib import Path

logo = "☁️"
PROJECT_NAME= '2lab'

def get_project_name(name):
    return '{} ({})'.format(name, PROJECT_NAME)

def get_project_category(sub_dirs = None):
    start = logo + PROJECT_NAME
    if sub_dirs is None:
        return start
    else:
        return "{}/{}".format(start,sub_dirs)

# PATH
comfyUI_root = Path(__file__).parent.parent.parent.parent
comfyUI_models_root = os.path.join(comfyUI_root,"models")
custom_nodes_root = Path(__file__).parent.parent.parent
project_root = Path(__file__).parent.parent
temp_folder = os.path.join(project_root,"temp")
javascript_folder = os.path.join(project_root,"js")
asset_folder = os.path.join(project_root,"asset")
# javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
# asset_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "asset")
myWorkflow_folder = os.path.join(project_root,"myWorkflow")
if not os.path.exists(myWorkflow_folder):
    os.makedirs(myWorkflow_folder)

# config
# config_file = os.path.join(project_root, 'config.json')
# config_template_file = os.path.join(project_root, 'config_template.json')

USER_KEY = None
auto_download_model = False
china_mirror = False

# read config from 2lab.ini
file_path = os.path.join(project_root, "2lab.ini")
# print("file_path ini = ", file_path)
if os.path.exists(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    config_key = config.get("auth", "user_key", fallback="")
    if config_key:
        config_key = config_key.strip()
        if config_key!="" and config_key!='YOUR_API_KEY':
            USER_KEY = config_key
    # print("USER_KEY from ini = ", USER_KEY)
    auto_download_model = config.get("download_models", "auto_download_model", fallback=False)
    china_mirror = config.get("download_models", "china_mirror", fallback=True)

# 其他py通过这里读取user key
def read_user_key(prompt):
    if USER_KEY and USER_KEY!="":
        return USER_KEY
    # 如果ini文件里没有user key，尝试从cookie读取
    try:
        # 这个url在ini文件里面指定
        data = {
            'prompt': json.dumps(prompt),
        }
        response = requests.post('http://127.0.0.1:8188/2lab/internal/readUserKey', data=data)
        print('read_user_key Response status:', response.status_code)
        print('read_user_key Response Content:', response.text)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常
        return response.text
    except:
        print(traceback.format_exc())
    return ''

# models
configs_folder = os.path.join(project_root, 'configs')
checkpoints_file = os.path.join(configs_folder, 'checkpoints.json')
lora_file = os.path.join(configs_folder, 'lora.json')
vae_file = os.path.join(configs_folder, 'vae.json')
controlnet_file = os.path.join(configs_folder, 'controlnet.json')
model_file = os.path.join(configs_folder, 'model.json')

checkpoints = []
if os.path.exists(checkpoints_file):
    with open(checkpoints_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            checkpoints.append(item['filename'])

loras = []
if os.path.exists(lora_file):
    with open(lora_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            loras.append(item['filename'])

vaes = []
if os.path.exists(vae_file):
    with open(vae_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            vaes.append(item['filename'])

controlnets = []
if os.path.exists(controlnet_file):
    with open(controlnet_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            controlnets.append(item['filename'])

models = {}
if os.path.exists(model_file):
    with open(model_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            models[item['custom_node']] = item

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


