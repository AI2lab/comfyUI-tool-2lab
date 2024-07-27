# NAMESPACE
import json
import os
import traceback
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
myWorkflow_folder = os.path.join(project_root,"myWorkflow")
if not os.path.exists(myWorkflow_folder):
    os.makedirs(myWorkflow_folder)

# config
config_file = os.path.join(project_root, 'config.json')
config_template_file = os.path.join(project_root, 'config_template.json')

# 如果配置文件不存在，则创建
config = json.load(open(config_template_file, 'r'))
if os.path.exists(config_file):
    try:
        with open(config_file, 'r') as file:
            config_exist = json.load(file)
            config.update(config_exist)
    except:
        print(traceback.format_exc())
try:
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)
except:
    print(traceback.format_exc())

# userKey
userKey_file = os.path.join(project_root, '2lab_key.txt')
def read_user_key()->str:
    if os.path.exists(userKey_file):
        with open(userKey_file, 'r', encoding='utf-8') as file:
            userKey = file.read().rstrip('\n')  # Remove the trailing newline
            return userKey
    return ""

# models
standardized_folder = os.path.join(project_root, 'standardized')
checkpoints_file = os.path.join(standardized_folder, 'checkpoints.json')
lora_file = os.path.join(standardized_folder, 'lora.json')
vae_file = os.path.join(standardized_folder, 'vae.json')
controlnet_file = os.path.join(standardized_folder, 'controlnet.json')
model_file = os.path.join(standardized_folder, 'model.json')

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

# print("checkpoints = ",checkpoints)
# print("loras = ",loras)
# print("vaes = ",vaes)
# print("controlnets = ",controlnets)
# print("models = ",models)
