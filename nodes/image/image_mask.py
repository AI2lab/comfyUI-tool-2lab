from ..constants import get_project_name,get_project_category

NODE_CATEGORY = get_project_category("image")

class MaskInvert:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "masks": ("MASK",),
            }
        }

    NAME = get_project_name('mask_invert')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("MASKS",)
    FUNCTION = "doWork"

    def doWork(self, masks):
        return (1. - masks,)
