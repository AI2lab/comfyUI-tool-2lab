import os.path
import zipfile
import subprocess
import traceback
import random
import qrcode
import requests
from tqdm import tqdm
from PIL import Image
from .constants import project_root, models, custom_nodes_root, comfyUI_models_root, china_mirror
import platform
from torchvision.datasets.utils import download_url


def truncate_string(s):
    # 查找 "/" 或 "\" 最后一次出现的位置
    index = max(s.rfind('/'), s.rfind('\\'))
    # 如果找到了至少一个分隔符，则截断字符串
    if index != -1:
        return s[index + 1:]  # 保留分隔符之后的部分
    else:
        return s  # 如果没有找到分隔符，返回原字符串

def filter_map(origin_list, filter_list):
    map = {}
    for item in origin_list:
        key = truncate_string(item)
        value = item
        map[key] = value
    # print("filter map :",map)
    filtered_map = {}
    for key, value in map.items():
        if key in filter_list:
            filtered_map[key] = value
    # print("filtered_map :",filtered_map)
    return filtered_map

def print_console(text):
    print(f"\033[34m[INFO]\033[0m {text}")
def print_error(text):
    print(f"\033[31m[ERROR]\033[0m {text}")