from ..common.sizes import get_image_size
from ..constants import get_project_name, get_project_category

from ..common import fields
import math
import comfy.utils   # comfyUI内部包

NODE_CATEGORY = get_project_category("image")

# fork from https://github.com/Derfuu/Derfuu_ComfyUI_ModdedNodes/, thx!
class ImageScale_Side:
    NAME = get_project_name('ImageScale_Side')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    upscale_methods = ["nearest-exact", "bilinear", "area"]
    crop_methods = ["disabled", "center"]

    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": fields.IMAGE,
                "side_length": fields.INT,
                "side": (["Longest", "Width", "Height"],),
                "upscale_method": (cls.upscale_methods,),
                "crop": (cls.crop_methods,)}}

    def doWork(self, image, upscale_method, side_length: int, side: str, crop):
        samples = image.movedim(-1, 1)

        size = get_image_size(image)

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
        else:
            width, height = determineSide(side)

        width = math.ceil(width)
        height = math.ceil(height)

        cls = comfy.utils.common_upscale(samples, width, height, upscale_method, crop)
        cls = cls.movedim(1, -1)
        return (cls,)

class CropImage:
    NAME = get_project_name('CropImage')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": fields.IMAGE_FORCEINPUT,
            }
        }

    def doWork(self, image):
        samples = image.movedim(-1, 1)
        # 获取原始尺寸
        old_width = samples.shape[3]
        old_height = samples.shape[2]

        # 计算剪裁尺寸
        min_size = min(old_width, old_height)
        print(min_size)

        # 计算剪裁起点
        x_start = (old_width - min_size) // 2
        y_start = (old_height - min_size) // 2

        # 执行中心剪裁
        cropped_image = samples[:, :, y_start:y_start + min_size, x_start:x_start + min_size]
        result_image = cropped_image.movedim(1, -1)

        return {"result": (result_image,)}

class WatermarkOffset:
    NAME = get_project_name('WatermarkOffset')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("xOffset", "yOffset",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": fields.IMAGE_FORCEINPUT,
                "watermarkImage": fields.IMAGE_FORCEINPUT,
                "location": (["top-left", "top-right", "bottom-left", "bottom-center", "bottom-right"],
                             {"default": "bottom-right"}),
                "margin_x": ("INT", {"default": 0}),
                "margin_y": ("INT", {"default": 0}),
            }
        }

    def doWork(self, image, watermarkImage, location, margin_x, margin_y):
        # 获取主图片和水印的尺寸
        _,  main_height,main_width, _ = image.shape
        _,  watermark_height,watermark_width, _ = watermarkImage.shape

        # print(main_width, main_height)
        # print(watermark_width, watermark_height)

        # 计算水印的偏移量
        if location == "top-left":
            xOffset = margin_x
            yOffset = margin_y
        elif location == "top-right":
            xOffset = main_width - watermark_width - margin_x
            yOffset = margin_y
        elif location == "bottom-left":
            xOffset = margin_x
            yOffset = main_height - watermark_height - margin_y
        elif location == "bottom-center":
            xOffset = int(margin_x/2)
            yOffset = main_height - watermark_height - margin_y
        elif location == "bottom-right":
            xOffset = main_width - watermark_width - margin_x
            yOffset = main_height - watermark_height - margin_y
        else:
            return {"result": (None, None,)}

        # print(location, xOffset, yOffset)

        # 检查偏移量是否合理
        if xOffset > 0 or main_width < xOffset or yOffset < 0 or yOffset > main_height:
            print("wrong x/y or x/yOffset")
            return {"result": (None, None,)}

        return {"result": (xOffset, yOffset,)}
