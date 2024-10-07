import math
from comfy.utils import common_upscale

from .constants import get_project_name, get_project_category, PROJECT_NAME

NODE_CATEGORY = get_project_category("image")

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
    Image_Scale_To_Ratio.NAME: Image_Scale_To_Ratio,
    Image_Scale_To_Side.NAME: Image_Scale_To_Side,
    ShowImageSizeAndCount.NAME: ShowImageSizeAndCount,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    Image_Scale_To_Ratio.NAME: "Image scale to ratio" + " (" + PROJECT_NAME + ")",
    Image_Scale_To_Side.NAME: "Image scale to side" + " (" + PROJECT_NAME + ")",
    ShowImageSizeAndCount.NAME: "Show image size & count" + " (" + PROJECT_NAME + ")",
}
