
import filecmp
import shutil
import os
import sys
import __main__
import importlib.util
import server
from aiohttp import web
from .nodes.constants import PROJECT_NAME, project_root, auto_download_model, javascript_folder, asset_folder

from .nodes.utils import download_model, print_console

python = sys.executable

WEB_DIRECTORY = "./js"
print_console("[comfyUI-tool-2lab] start")

# User extension files in custom_nodes
# project_name = PROJECT_NAME
# extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
#                                  "web" + os.sep + "extensions" + os.sep + project_name)

# if not os.path.exists(extentions_folder):
#     os.mkdir(extentions_folder)
#
# result = filecmp.dircmp(javascript_folder, extentions_folder)
#
# if result.left_only or result.diff_files:
#     file_list = list(result.left_only)
#     file_list.extend(x for x in result.diff_files if x not in file_list)
#
#     for file in file_list:
#         src_file = os.path.join(javascript_folder, file)
#         dst_file = os.path.join(extentions_folder, file)
#         if os.path.exists(dst_file):
#             os.remove(dst_file)
#         shutil.copy(src_file, dst_file)

# # 如果user key不存在，创建
# userKey = None
# if not os.path.exists(userKey_file):
#     try:
#         # allocate user key from server
#         command = "engine_wx2lab_create_user_key"
#         paramMap = {}
#         responseJson = submit(command, json.dumps(paramMap))
#         print("create new user key : ",responseJson)
#         if responseJson and responseJson['success'] and responseJson['data']:
#             userKey = responseJson['data']['userKey']
#             # 覆盖userKey
#             with open(userKey_file, 'w', encoding='utf-8') as file:
#                 file.write(userKey)
#     except:
#         print(traceback.format_exc())
#         pass
# else:
#     userKey = read_user_key()

# 如果QRcode不存在，创建
# qr_file_path = os.path.join(project_root, "2lab_key.png")
# if userKey is not None and not os.path.exists(qr_file_path):
#     url = "https://www.2lab.cn/wx2lab/bind/" + userKey
#     print("creating QR code picture : ",url)
#     create_qr_code(url, qr_file_path)

# 如果config中指定自动下载模型，则执行下载
if auto_download_model:
    download_model('')

def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

py = get_ext_dir("nodes")
files = os.listdir(py)
for file in files:
    if not file.endswith(".py"):
        continue
    name = os.path.splitext(file)[0]
    imported_module = importlib.import_module(".nodes.{}".format(name), __name__)
    try:
        NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
        NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}
    except:
        pass

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

@server.PromptServer.instance.routes.get("/2lab/readKeyFromCookie")
async def get_key_from_cookie(request):
    cookies = request.cookies
    if cookies:
        print (f'Cookies: {cookies}')
    else:
        print ('No cookies found')

    user_key = request.cookies.get("2lab_user_key")
    print("readKeyFromCookie - user_key = ",user_key)
    if not user_key:
        user_key = ''
    return web.Response(text=user_key, content_type="text/html")

print_console("[comfyUI-tool-2lab] finished")