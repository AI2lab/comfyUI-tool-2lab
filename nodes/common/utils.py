import os
import time

import requests
from ..constants import temp_folder

def downloadFileToTempFolder(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()

        try:
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
        except Exception as e:
            print(f"Fail to create directory '{temp_folder}. Error: {e}'")
            return None

        # temp file name
        ext = getFileNameExt(url)
        curtime = str(int(time.time()))
        filename = curtime
        if curtime != "":
            filename = curtime+"."+ext
        file_path = os.path.join(temp_folder,filename)
    except:
        return ''
    return file_path

def getFileNameExt(fileName: str) -> str:
    try:
        # 分割文件名，获取后缀名
        ext = ""
        parts = fileName.split('.')
        # 如果没有后缀名或文件名本身就是以'.'开头（例如隐藏文件），返回空字符串
        if len(parts) >= 2:
            # 返回最后一个部分作为后缀名
            ext = parts[-1]
        else:
            ext = ""
        return ext
    except:
        return ""
