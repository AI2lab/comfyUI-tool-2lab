# fork from https://github.com/Derfuu/Derfuu_ComfyUI_ModdedNodes/, thx!

import sys

FLOAT = ("FLOAT", {"default": 1,
                   "min": -sys.float_info.max,
                   "max": sys.float_info.max,
                   "step": 0.01})
BOOL_TRUE = ("BOOLEAN", {"default": True})
BOOL_FALSE = ("BOOLEAN", {"default": False})
INT = ("INT", {"default": 1,
               "min": -sys.maxsize,
               "max": sys.maxsize,
               "step": 1})
INT_POSITIVE = ("INT", {"default": 1,
               "min": 1,
               "max": sys.maxsize,
               "step": 1})
STRING = ("STRING", {"default": ""})
STRING_ML = ("STRING", {"multiline": True, "default": ""})
IMAGE = ("IMAGE",)
IMAGE_FORCEINPUT = ("IMAGE", {"forceInput": True})