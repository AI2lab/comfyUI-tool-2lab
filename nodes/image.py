import math
import os
import random

import requests
from io import BytesIO
from .constants import get_project_name, get_project_category, PROJECT_NAME
import folder_paths
from comfy.utils import common_upscale
from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import torch
import hashlib

NODE_CATEGORY = get_project_category("image")

class LoadImageByPath:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {
                        "image_path": ("STRING", {"multiline": False, "default": ''}),
                     },
                }

    NAME = get_project_name('LoadImageByPath')
    CATEGORY = NODE_CATEGORY

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"

    def load_image(self, image_path):
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return (output_image, output_mask)

    @classmethod
    def IS_CHANGED(s, image_path):
        m = hashlib.sha256()
        m.update(image_path)
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image_path):
        if not os.path.exists(image_path):
            return "Invalid image path: {}".format(image_path)
        return True

class SaveImageByUrl:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
                {"image_urls": ("LIST", {"forceInput": True}),
                 "filename_prefix": ("STRING", {"default": "2lab/img"}),
                 },
        }

    NAME = get_project_name('SaveImageByUrl')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ()
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    def doWork(self, image_urls, filename_prefix="2lab/img" ):
        filename_prefix += self.prefix_append
        # print(f"image_urls = {image_urls}")
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        results = list()
        for (batch_number, image_url) in enumerate(image_urls):
            # print(f"{batch_number} : {image_url}")
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            image_path = os.path.join(full_output_folder, file)
            # print(f"image_path = {image_path}")
            if download_image(image_url, image_path):
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
        return { "ui": { "images": results } }

class PreviewImageByUrl(SaveImageByUrl):
    NAME = get_project_name('PreviewImageByUrl')
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
        self.compress_level = 1

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"image_urls": ("LIST", {"forceInput": True}),},
                }
def download_image(url, save_path)->bool:
    compress_level = 4

    # 发送HTTP GET请求获取图片数据
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 将响应内容转换为图片对象
        image = Image.open(BytesIO(response.content))

        # 保存图片到本地
        image.save(save_path, compress_level=compress_level)
        print(f"图片已保存到 {save_path}")
        return True
    else:
        print(f"下载图片失败，状态码: {response.status_code}")
    return False


class SaveVideoByUrl:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        # self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
                {"video_urls": ("LIST", {"forceInput": True}),
                 "filename_prefix": ("STRING", {"default": "2lab/video"}),
                 },
        }

    NAME = get_project_name('SaveVideoByUrl')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ()
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    def doWork(self, video_urls, filename_prefix="2lab/video" ):
        filename_prefix += self.prefix_append
        print(f"video_urls = {video_urls}")
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        results = list()
        for (batch_number, video_url) in enumerate(video_urls):
            print(f"{batch_number} : {video_url}")
            ext = video_url.rsplit('.', 1)[1]
            print(f"filename : {filename}")
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_."+ext
            video_path = os.path.join(full_output_folder, file)
            print(f"video_path = {video_path}")
            if download_video(video_url, video_path):
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
        print(f"results = {results}")
        return { "ui": { "images": results } }

def download_video(url, save_path)->bool:
    # 发送HTTP GET请求获取视频数据
    response = requests.get(url, stream=True)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开文件以二进制写入模式
        with open(save_path, 'wb') as file:
            # 将响应内容写入文件
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"视频已保存到 {save_path}")
        return True
    else:
        print(f"下载视频失败，状态码: {response.status_code}")
    return False

class SaveImageByPath:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
                {"image_paths": ("LIST", {"forceInput": True}),
                 "filename_prefix": ("STRING", {"default": "2lab/img"}),
                 },
        }

    NAME = get_project_name('SaveImageByPath')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ()
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    def doWork(self, image_paths, filename_prefix="2lab/img" ):
        filename_prefix += self.prefix_append
        print(f"image_paths = {image_paths}")
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        results = list()
        for (batch_number, image_path) in enumerate(image_paths):
            print(f"{batch_number} : {image_path}")
            with Image.open(image_path) as img:
                filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
                file = f"{filename_with_batch_num}_{counter:05}_.png"
                img.save(os.path.join(full_output_folder, file), compress_level=self.compress_level)
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
                counter += 1
        return { "ui": { "images": results } }

class PreviewImageByPath(SaveImageByPath):
    NAME = get_project_name('PreviewImageByPath')
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
        self.compress_level = 1

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"image_paths": ("LIST", {"forceInput": True}),},
                }

class Image_Scale_To_Ratio:
    NAME = get_project_name('Image_Scale_To_Ratio')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_NAMES = ("image", )
    RETURN_TYPES = ("IMAGE",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_by": ("FLOAT", {"default": 1.0, "min": 0, "max": 100.0, "step": 0.1}),
                "side_length": ("INT", {"default": 1024, "min": 1, "max": 0xffffffffffffffff}),
                "upscale_method": (["nearest-exact", "bilinear", "bicubic", "bislerp", "area", "lanczos"], {"default": "nearest-exact"}),
                "crop": (["disabled", "center"], {"default": "disabled"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"

    def doWork(self, image, upscale_method, upscale_by, crop):
        samples = image.movedim(-1, 1)
        size = samples.shape[3], samples.shape[2]

        width_B = int(size[0])
        height_B = int(size[1])

        samples = image.movedim(-1, 1)

        height = math.ceil(height_B * upscale_by)
        width = math.ceil(width_B * upscale_by)
        cls = common_upscale(samples, width, height, upscale_method, crop)
        cls = cls.movedim(1, -1)
        return (cls,)

class Image_Scale_To_Side:
    NAME = get_project_name('Image_Scale_To_Side')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_NAMES = ("image", )
    RETURN_TYPES = ("IMAGE",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "side_length": ("INT", {"default": 1024, "min": 1, "max": 0xffffffffffffffff}),
                "side": (["Longest", "Shortest", "Width", "Height"], {"default": "Longest"}),
                "upscale_method": (["nearest-exact", "bilinear", "bicubic", "bislerp", "area", "lanczos"], {"default": "nearest-exact"}),
                "crop": (["disabled", "center"], {"default": "disabled"}),
            }
        }

    def doWork(self, image, upscale_method, side_length: int, side: str, crop):
        samples = image.movedim(-1, 1)
        size = samples.shape[3], samples.shape[2]

        width_B = int(size[0])
        height_B = int(size[1])

        width = width_B
        height = height_B

        def determineSide(_side: str) -> tuple[int, int]:
            width, height = 0, 0
            if _side == "Width":
                heigh_ratio = height_B / width_B
                width = side_length
                height = heigh_ratio * width
            elif _side == "Height":
                width_ratio = width_B / height_B
                height = side_length
                width = width_ratio * height
            return width, height

        if side == "Longest":
            if width > height:
                width, height = determineSide("Width")
            else:
                width, height = determineSide("Height")
        elif side == "Shortest":
            if width < height:
                width, height = determineSide("Width")
            else:
                width, height = determineSide("Height")
        else:
            width, height = determineSide(side)

        width = math.ceil(width)
        height = math.ceil(height)

        cls = common_upscale(samples, width, height, upscale_method, crop)
        cls = cls.movedim(1, -1)
        return (cls,)

class ShowImageSizeAndCount:
    NAME = get_project_name('ShowImageSizeAndCount')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_TYPES = ("IMAGE","INT", "INT", "INT",)
    RETURN_NAMES = ("image", "width", "height", "count",)
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE",),
        }}

    def doWork(self, image):
        width = image.shape[2]
        height = image.shape[1]
        count = image.shape[0]
        return {"ui": {
            "text": [f"width x height : {width} x {height}\nimage count : {count}"]},
            "result": (image, width, height, count)
        }

NODE_CLASS_MAPPINGS = {
    LoadImageByPath.NAME: LoadImageByPath,
    SaveImageByPath.NAME: SaveImageByPath,
    PreviewImageByPath.NAME: PreviewImageByPath,
    SaveImageByUrl.NAME: SaveImageByUrl,
    PreviewImageByUrl.NAME: PreviewImageByUrl,
    SaveVideoByUrl.NAME: SaveVideoByUrl,


    Image_Scale_To_Ratio.NAME: Image_Scale_To_Ratio,
    Image_Scale_To_Side.NAME: Image_Scale_To_Side,
    ShowImageSizeAndCount.NAME: ShowImageSizeAndCount,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    LoadImageByPath.NAME: "Load Image By Path" + " (" + PROJECT_NAME + ")",
    SaveImageByPath.NAME: "Save Image By Path" + " (" + PROJECT_NAME + ")",
    PreviewImageByPath.NAME: "Preview Image By Path" + " (" + PROJECT_NAME + ")",
    SaveImageByUrl.NAME: "Save Image By Url" + " (" + PROJECT_NAME + ")",
    PreviewImageByUrl.NAME: "Preview Image By Url" + " (" + PROJECT_NAME + ")",
    SaveVideoByUrl.NAME: "Save Video By Url" + " (" + PROJECT_NAME + ")",
    Image_Scale_To_Ratio.NAME: "Image scale to ratio" + " (" + PROJECT_NAME + ")",
    Image_Scale_To_Side.NAME: "Image scale to side" + " (" + PROJECT_NAME + ")",
    ShowImageSizeAndCount.NAME: "Show image size & count" + " (" + PROJECT_NAME + ")",
}
