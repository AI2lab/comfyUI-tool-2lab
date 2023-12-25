from ..constants import get_name,get_category

class MaskInvert:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
                    "required": {
                        "masks": ("MASK",),
                    }
                }

    NAME = get_name('mask_invert')
    CATEGORY = get_category("image")
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("MASKS",)
    FUNCTION = "doWork"

    def doWork(self, masks):
        return (1. - masks,)
