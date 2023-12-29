import numpy as np
import torch
from PIL import Image

from ..common.utils import downloadFileToTempFolder
from ..constants import get_project_name, get_project_category

NODE_CATEGORY = get_project_category("util/preview")

class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",},
        }

    NAME = get_project_name('show_text')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    def doWork(self, string, unique_id=None, extra_pnginfo=None):
        return {"ui": {"string": [string, ]}, "result": (string,)}

class ShowWebImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_url": ("STRING", {"multiline": False}),
                "RGBA": (["false", "true"],{"default":False}),
            },
        }

    NAME = get_project_name('show_web_image')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("IMAGE", "MASK","TEXT","filePath")
    RETURN_NAMES = ("image", "mask","image_url","filePath")
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    def doWork(self, image_url, RGBA):
        print(image_url)
        i = None
        file_path = ''
        try:
            if image_url.startswith('http'):
                file_path,i = self.download_image(image_url)
            else:
                file_path = image_url
                i = Image.open(image_url)

            if not i:
                return

            image = i
            if not RGBA:
                image = image.convert('RGB')
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            # RGBA - mask
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            return (image, mask, image_url,file_path)

        except :
            pass
        return (None, None, image_url,file_path)

    def download_image(self, url):
        file_path = downloadFileToTempFolder(url)
        if file_path == '':
            return file_path,None
        else:
            img = Image.open(file_path)
            return file_path,img
