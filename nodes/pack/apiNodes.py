import json
import os
import requests
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import comfy.sd
import comfy.utils
from comfy.cli_args import args
import folder_paths
import torch
import hashlib
from ..api.caller import submit

from ..constants import get_project_name, get_project_category, read_user_key, myWorkflow_folder, \
    checkpoints, loras, vaes, controlnets
from PIL.PngImagePlugin import PngInfo

from ..utils import truncate_string, filter_list

NODE_CATEGORY = get_project_category("pack")

MAX_TEXT_LENGTH = 30


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class InputImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True}),
                     "desc": ("STRING", {"default": "图片", "multiline": False}),
                     "export": ("BOOLEAN", {"default": True}),
                     },
                }

    NAME = get_project_name('InputImage')
    CATEGORY = NODE_CATEGORY

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"

    def load_image(self, image, desc, export):
        image_path = folder_paths.get_annotated_filepath(image)
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
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True


class InputSeed:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            "export": ("BOOLEAN", {"default": True}),
        },
        }

    NAME = get_project_name('InputSeed')
    CATEGORY = NODE_CATEGORY

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    @staticmethod
    def doWork(seed, export):
        return seed,


class InputText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING", {"default": "", "multiline": True}),
            "type": (["short"], {"default": "short"}),
            "desc": ("STRING", {"default": "提示词", "multiline": False}),
            "export": ("BOOLEAN", {"default": True}),
        },
        }

    NAME = get_project_name('InputText')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @staticmethod
    def doWork(text, type, desc, export):
        # 只允许不超过20字的输入，用于seg或艺术字
        # 长prompt应该作为模版输入
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(f"text too long. max length is {MAX_TEXT_LENGTH}")
        return text,


class InputChoice:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING", {"default": "", "multiline": False}),
            "options": ("STRING", {"default": "", "multiline": True}),
            "desc": ("STRING", {"default": "选项", "multiline": False}),
            "export": ("BOOLEAN", {"default": True}),
        },
        }

    NAME = get_project_name('InputChoice')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @staticmethod
    def doWork(text, options, desc, export):
        print("text = ", text)
        print("options = ", options)
        optionList = options.split("|")
        if text not in optionList:
            raise ValueError(f"{text} not found in options. options should use '|' as the delimiter")
        return text,


class InputWildCard:
    cardMap = {}

    @classmethod
    def INPUT_TYPES(c):
        return {"required": {
            "text": ("STRING", {"default": "", "multiline": False}),
            "wildcard": (c.get_wildcard_list(),),
            "desc": ("STRING", {"default": "选项", "multiline": False}),
            "export": ("BOOLEAN", {"default": True}),
        },
        }

    NAME = get_project_name('InputChoice')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doWork"

    @staticmethod
    def doWork(text, options, desc, export):
        optionList = options.split("|")
        if text not in optionList:
            raise ValueError(f"{text} not found in options. options should use '|' as the delimiter")
        return text,

    @staticmethod
    def get_wildcard_list():
        pass

    def read_wildcard(self, cardId):
        command = "engine_image_read_wildcard"
        paramMap = {
            'cardId': cardId,
        }
        responseJson = submit(command, json.dumps(paramMap))
        # print(responseJson)
        if responseJson['success'] == True and responseJson['data']:
            result = responseJson['data']
            self.cardMap[cardId] = result
            return result
        else:
            return {}


class OutputText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    NAME = get_project_name('OutputText')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"
    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True

    def doWork(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif (
                    not isinstance(extra_pnginfo[0], dict)
                    or "workflow" not in extra_pnginfo[0]
            ):
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [text]

        return {"ui": {"text": text}, "result": (text,)}


class OutputImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
                {"images": ("IMAGE",),
                 "filename_prefix": ("STRING", {"default": "2lab/img"}),
                 "metadata": (["disable", "enable"], {"default": "disable"})},
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    NAME = get_project_name('OutputImage')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    def doWork(self, images, filename_prefix="2lab/img", metadata="disable", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        # print("filename_prefix = ",filename_prefix)
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])

        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if (not args.disable_metadata) and (metadata == "enable"):
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return {"ui": {"images": results}, "result": (json.dumps(prompt),)}


class CheckpointLoader:
    def __init__(self):
        # for test
        ckpts = folder_paths.get_filename_list("checkpoints")
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"ckpt_name": (filter_list(folder_paths.get_filename_list("checkpoints"),checkpoints),),
                             }
                }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    NAME = get_project_name('CheckpointLoader')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"

    def doWork(self, ckpt_name):
        simple_ckpt_name = truncate_string(ckpt_name)
        if simple_ckpt_name in checkpoints:
            print("simple_ckpt_name in checkpoints")
        else:
            msg = f"checkpoint '{simple_ckpt_name}' not in available list, please check model.json"
            raise ValueError(msg)

        ckptList = folder_paths.get_filename_list("checkpoints")
        # print("ckptList = ",ckptList)
        for ckpt_path_item in ckptList:
            simple_file_name = truncate_string(ckpt_path_item)
            if simple_file_name == simple_ckpt_name:
                ckpt_name = ckpt_path_item
                # print("simple_file_name = ",simple_file_name)
                # print("ckpt_name full = ",ckpt_name)
                break
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True,
                                                    embedding_directory=folder_paths.get_folder_paths("embeddings"))
        return out[:3]


class LoraLoader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model": ("MODEL",),
                             "clip": ("CLIP",),
                             "lora_name": (filter_list(folder_paths.get_filename_list("loras"),loras),),
                             "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             "strength_clip": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                             }
                }

    RETURN_TYPES = ("MODEL", "CLIP")
    NAME = get_project_name('LoraLoader')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"

    def doWork(self, model, clip, lora_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0:
            return (model, clip)

        simple_lora_name = truncate_string(lora_name)
        if simple_lora_name in loras:
            print("simple_ckpt_name in loras")
        else:
            msg = f"checkpoint '{simple_lora_name}' not in available list, please check lora.json"
            raise ValueError(msg)

        loraList = folder_paths.get_filename_list("loras")
        # print("loraList = ",loraList)
        for lora_path_item in loraList:
            simple_file_name = truncate_string(lora_path_item)
            if simple_file_name == simple_lora_name:
                lora_name = lora_path_item
                print("simple_file_name = ",simple_file_name)
                print("lora_name full = ",lora_name)
                break

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return (model_lora, clip_lora)


class VAELoader:
    @staticmethod
    def vae_list():
        vaes = folder_paths.get_filename_list("vae")
        approx_vaes = folder_paths.get_filename_list("vae_approx")
        sdxl_taesd_enc = False
        sdxl_taesd_dec = False
        sd1_taesd_enc = False
        sd1_taesd_dec = False

        for v in approx_vaes:
            if v.startswith("taesd_decoder."):
                sd1_taesd_dec = True
            elif v.startswith("taesd_encoder."):
                sd1_taesd_enc = True
            elif v.startswith("taesdxl_decoder."):
                sdxl_taesd_dec = True
            elif v.startswith("taesdxl_encoder."):
                sdxl_taesd_enc = True
        if sd1_taesd_dec and sd1_taesd_enc:
            vaes.append("taesd")
        if sdxl_taesd_dec and sdxl_taesd_enc:
            vaes.append("taesdxl")
        return vaes

    @staticmethod
    def load_taesd(name):
        sd = {}
        approx_vaes = folder_paths.get_filename_list("vae_approx")

        encoder = next(filter(lambda a: a.startswith("{}_encoder.".format(name)), approx_vaes))
        decoder = next(filter(lambda a: a.startswith("{}_decoder.".format(name)), approx_vaes))

        enc = comfy.utils.load_torch_file(folder_paths.get_full_path("vae_approx", encoder))
        for k in enc:
            sd["taesd_encoder.{}".format(k)] = enc[k]

        dec = comfy.utils.load_torch_file(folder_paths.get_full_path("vae_approx", decoder))
        for k in dec:
            sd["taesd_decoder.{}".format(k)] = dec[k]

        if name == "taesd":
            sd["vae_scale"] = torch.tensor(0.18215)
        elif name == "taesdxl":
            sd["vae_scale"] = torch.tensor(0.13025)
        return sd

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"vae_name": (filter_list(s.vae_list(),vaes),)}}

    RETURN_TYPES = ("VAE",)
    FUNCTION = "doWork"
    NAME = get_project_name('VaeLoader')
    CATEGORY = NODE_CATEGORY

    def doWork(self, vae_name):
        if vae_name in ["taesd", "taesdxl"]:
            sd = self.load_taesd(vae_name)
        else:
            vae_path = folder_paths.get_full_path("vae", vae_name)
            simple_vae_name = truncate_string(vae_name)
            if simple_vae_name in vaes:
                print("simple_vae_name in vaes")
            else:
                msg = f"checkpoint '{simple_vae_name}' not in available list, please check vae.json"
                raise ValueError(msg)
            sd = comfy.utils.load_torch_file(vae_path)
        vae = comfy.sd.VAE(sd=sd)
        return (vae,)


class ControlNetLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"control_net_name": (filter_list(folder_paths.get_filename_list("controlnet"),controlnets),)} }

    RETURN_TYPES = ("CONTROL_NET",)
    NAME = get_project_name('ControlNetLoader')
    CATEGORY = NODE_CATEGORY
    FUNCTION = "doWork"

    def doWork(self, control_net_name):
        # print("control_net_name = ",control_net_name)
        simple_cn_name = truncate_string(control_net_name)
        if simple_cn_name in controlnets:
            print("simple_cn_name in controlnets")
        else:
            msg = f"checkpoint '{simple_cn_name}' not in available list, please check controlnet.json"
            raise ValueError(msg)

        cnList = folder_paths.get_filename_list("controlnet")
        # print("cnList = ",cnList)
        for cn_path_item in cnList:
            simple_file_name = truncate_string(cn_path_item)
            if simple_file_name == simple_cn_name:
                control_net_name = cn_path_item
                # print("simple_file_name = ",simple_file_name)
                # print("control_net_name full = ",control_net_name)
                break

        controlnet_path = folder_paths.get_full_path("controlnet", control_net_name)
        controlnet = comfy.controlnet.load_controlnet(controlnet_path)
        return (controlnet,)




class PublishWorkflow:
    def __init__(s):
        pass

    @classmethod
    def INPUT_TYPES(c):
        return {
            "required": {
                "trigger": (any, {}),
                "id": ("STRING", {"default": "workflowId", "multiline": False}),
                "name": ("STRING", {"default": "文生图", "multiline": False}),
                "desc": ("STRING", {"default": "", "multiline": False}),
                "publish": ("BOOLEAN", {"default": False}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    NAME = get_project_name('PublishWorkflow')
    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("BOOL", "STRING",)
    RETURN_NAMES = ("publish", "id",)
    FUNCTION = "doWork"
    OUTPUT_NODE = True

    def doWork(self, id, name, desc, publish, trigger=None, prompt=None, extra_pnginfo=None):
        # print("extra_pnginfo = ",extra_pnginfo)
        # print("prompt = ",prompt)

        text = ''
        if publish:
            workflow = prompt
            # 保存本地备份
            file_path = os.path.join(myWorkflow_folder, id + '.json')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(workflow))

            userKey = read_user_key()
            print(f"userKey = [{userKey}]")
            if userKey == '':
                text = '未找到开发密钥，请把example目录中的 input_key.png拖入comfyUI界面，输入开发密钥后，点击浮动菜单上的Queue Prompt按钮保存密钥到2lab_key.txt'
            else:
                body = {
                    'userKey': userKey,
                    'workflow': workflow
                }
                print(body)

                url = "https://api.factx.cn/api/v4/i?c=engine_image_upload_workflow";
                print("url = ", url)
                headers = {
                    'content-type': 'application/json;charset=utf-8',
                }
                response = requests.post(url, headers=headers, data=json.dumps(body))
                print("response = ", response.text)
                resJson = json.loads(response.text)
                print("resJson = ", resJson)
                if resJson["success"]:
                    # share_url = resJson["data"]["url"],
                    text = f'工作流已经上传到服务器，请稍后到小程序中使用，服务器处理工作流需要几分钟，请耐心等待。如果有疑问，请请到http://www.2lab.cn/pb/contactus 咨询技术支持。'
                    raise ValueError(f'工作流上传完成，终止工作流运行。如果要正常运行工作流，请把publish改回false')
                else:
                    msg =  f'发布失败，原因：{resJson["message"]}'
                    raise ValueError(msg)
        else:
            text = '项目未发布。如果要发布本工作流到网页，请把参数publish设为True'

        return {"ui": {"text": [text, ]}, "result": (publish, id,)}
