
import filecmp
import shutil
import os
import sys
import __main__
import importlib.util
import server
from aiohttp import web
from .nodes.constants import PROJECT_NAME, project_root, auto_download_model, javascript_folder, asset_folder

from .nodes.utils import  print_console

python = sys.executable

WEB_DIRECTORY = "./js"
print_console("[comfyUI-tool-2lab] start")

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

# @server.PromptServer.instance.routes.get("/2lab/readKeyFromCookie")
# async def get_key_from_cookie(request):
#     cookies = request.cookies
#     if cookies:
#         print (f'Cookies: {cookies}')
#     else:
#         print ('No cookies found')
#
#     user_key = request.cookies.get("2lab_user_key")
#     print("readKeyFromCookie - user_key = ",user_key)
#     if not user_key:
#         user_key = ''
#     return web.Response(text=user_key, content_type="text/html")

print_console("[comfyUI-tool-2lab] finished")