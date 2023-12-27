import numpy as np
import requests
import torch
from PIL import Image
from io import BytesIO
from ..constants import get_project_name,get_project_category

NODE_CATEGORY = get_project_category("util/preview")

class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",},
        }

    NAME = get_project_name('show_text')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    def doWork(self, text, unique_id=None, extra_pnginfo=None):
        return {"ui": {"string": [text, ]}, "result": (text,)}

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
    RETURN_TYPES = ("IMAGE", "MASK","TEXT")
    RETURN_NAMES = ("image", "mask","image_url")
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    def doWork(self, image_url, RGBA):
        print(image_url)
        url = ""
        if image_url.startswith('http'):
            url = image_url
            from io import BytesIO
            i = self.download_image(image_url)
        else:
            try:
                i = Image.open(image_url)
            except OSError:
                # cstr(f"The image `{image_path.strip()}` specified doesn't exist!").error.print()
                # i = Image.new(mode='RGB', size=(512, 512), color=(0, 0, 0))
                return
        if not i:
            return
        print(url)
        print(i.size)

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

        return (image, mask, url)

    def download_image(self, url):
        print(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            print(img.size)
            return img
        except:
            return None
