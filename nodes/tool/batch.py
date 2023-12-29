import sys

import torch

from ..common import fields
from ..constants import get_project_name, get_project_category
NODE_CATEGORY = get_project_category("util/batch")
import comfy.utils  # comfyUI内部包

class ImageBatch9:
    NAME = get_project_name('ImageBatch9')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
                {
                    "image1": ("IMAGE",),
                    "image2": ("IMAGE",),
                },
            "optional":
                {
                    "image3": ("IMAGE",),
                    "image4": ("IMAGE",),
                    "image5": ("IMAGE",),
                    "image6": ("IMAGE",),
                    "image7": ("IMAGE",),
                    "image8": ("IMAGE",),
                    "image9": ("IMAGE",),
                }
        }

    def doWork(self, image1, image2, image3=None, image4=None, image5=None, image6=None, image7=None, image8=None,
               image9=None):

        if image1.shape[1:] != image2.shape[1:]:
            image2 = comfy.utils.common_upscale(image2.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image3 is not None and image1.shape[1:] != image3.shape[1:]:
            image3 = comfy.utils.common_upscale(image3.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image4 is not None and image1.shape[1:] != image4.shape[1:]:
            image4 = comfy.utils.common_upscale(image4.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image5 is not None and image1.shape[1:] != image5.shape[1:]:
            image5 = comfy.utils.common_upscale(image5.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image6 is not None and image1.shape[1:] != image6.shape[1:]:
            image6 = comfy.utils.common_upscale(image6.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image7 is not None and image1.shape[1:] != image7.shape[1:]:
            image7 = comfy.utils.common_upscale(image7.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image8 is not None and image1.shape[1:] != image8.shape[1:]:
            image8 = comfy.utils.common_upscale(image8.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        if image9 is not None and image1.shape[1:] != image9.shape[1:]:
            image9 = comfy.utils.common_upscale(image9.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear",
                                                "center").movedim(1, -1)

        list = [image1, image2]
        if image3 is not None:
            list.append(image3)
        if image4 is not None:
            list.append(image4)
        if image5 is not None:
            list.append(image5)
        if image6 is not None:
            list.append(image6)
        if image7 is not None:
            list.append(image7)
        if image8 is not None:
            list.append(image8)
        if image9 is not None:
            list.append(image9)

        print("list : ", len(list))

        s = torch.cat(tuple(list), dim=0)
        # s = torch.cat((image1, image2, image3, image4, image5, image6, image7, image8, image9), dim=0)
        return (s,)


class LatentBatch9:
    NAME = get_project_name('LatentBatch9')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("image",)
    OUTPUT_NODE = True
    FUNCTION = "doWork"

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"samples1": ("LATENT",),
                     "samples2": ("LATENT",),
                     },
                "optional":
                    {
                        "samples3": ("LATENT",),
                        "samples4": ("LATENT",),
                        "samples5": ("LATENT",),
                        "samples6": ("LATENT",),
                        "samples7": ("LATENT",),
                        "samples8": ("LATENT",),
                        "samples9": ("LATENT",),
                    }

                }

    def doWork(self, samples1, samples2, samples3=None, samples4=None, samples5=None, samples6=None, samples7=None, samples8=None, samples9=None):
        samples_out = samples1.copy()
        s1 = samples1["samples"]
        s2 = samples2["samples"]

        s3 = None
        if samples3 is not None:
            s3 = samples3["samples"]

        s4 = None
        if samples4 is not None:
            s4 = samples4["samples"]

        s5 = None
        if samples5 is not None:
            s5 = samples5["samples"]

        s6 = None
        if samples6 is not None:
            s6 = samples6["samples"]

        s7 = None
        if samples7 is not None:
            s7 = samples7["samples"]

        s8 = None
        if samples8 is not None:
            s8 = samples8["samples"]

        s9 = None
        if samples9 is not None:
            s9 = samples9["samples"]

        if s1.shape[1:] != s2.shape[1:]:
            s2 = comfy.utils.common_upscale(s2, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s3 is not None and s1.shape[1:] != s3.shape[1:]:
            s3 = comfy.utils.common_upscale(s3, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s4 is not None and s1.shape[1:] != s4.shape[1:]:
            s4 = comfy.utils.common_upscale(s4, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s5 is not None and s1.shape[1:] != s5.shape[1:]:
            s5 = comfy.utils.common_upscale(s5, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s6 is not None and s1.shape[1:] != s6.shape[1:]:
            s6 = comfy.utils.common_upscale(s6, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s7 is not None and s1.shape[1:] != s7.shape[1:]:
            s7 = comfy.utils.common_upscale(s7, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s8 is not None and s1.shape[1:] != s8.shape[1:]:
            s8 = comfy.utils.common_upscale(s8, s1.shape[3], s1.shape[2], "bilinear", "center")
        if s9 is not None and s1.shape[1:] != s9.shape[1:]:
            s9 = comfy.utils.common_upscale(s9, s1.shape[3], s1.shape[2], "bilinear", "center")

        list = [s1, s2]
        if s3 is not None:
            list.append(s3)
        if s4 is not None:
            list.append(s4)
        if s5 is not None:
            list.append(s5)
        if s6 is not None:
            list.append(s6)
        if s7 is not None:
            list.append(s7)
        if s8 is not None:
            list.append(s8)
        if s9 is not None:
            list.append(s9)

        print("list : ", len(list))

        s = torch.cat(tuple(list), dim=0)
        # s = torch.cat((s1, s2, s3, s4, s5, s6, s7, s8, s9), dim=0)
        samples_out["samples"] = s
        samples_out["batch_index"] = samples1.get("batch_index", [x for x in range(0, s1.shape[0])]) + samples2.get("batch_index", [x for x in range(0, s2.shape[0])])
        if s3 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples3.get("batch_index", [x for x in range(0, s3.shape[0])])
        if s4 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples4.get("batch_index", [x for x in range(0, s4.shape[0])])
        if s5 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples5.get("batch_index", [x for x in range(0, s5.shape[0])])
        if s6 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples6.get("batch_index", [x for x in range(0, s6.shape[0])])
        if s7 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples7.get("batch_index", [x for x in range(0, s7.shape[0])])
        if s8 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples8.get("batch_index", [x for x in range(0, s8.shape[0])])
        if s9 is not None:
            samples_out["batch_index"] = samples_out["batch_index"] + samples9.get("batch_index", [x for x in range(0, s9.shape[0])])
        return (samples_out,)
