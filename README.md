# comfyUI-tool-2lab

# 项目介绍 
本项目的目标是帮助中国comfyUI开发者更方便地建立个人站点和商店
- 手机使用：把comfyUI与微信绑定，可以在手机上启动绘图任务，也可以直接加工手机拍摄的照片
- 快速发布：从comfyUI一键发布绘图模版到云服务器
- 朋友分享：通过微信小程序分享工作流和作品给朋友
- 节省流量：自动根据插件从国内站点下载模型大文件

## 有限支持
- 本系统依赖于comfyUI及其开源插件社区。由于开源系统的特点，插件之间容易出现冲突。本系统将支持大部分主流插件和模型，但不会支持所有插件和模型。
- 本系统专门为中国用户服务，部分核心功能在微信小程序中实现，也会尽量下载模型文件的流量问题。

# 使用方法

## 安装
1. 安装插件comfyUI-tool-2lab后， 当comfyUI再次启动时，comfyUI-tool-2lab会自动完成初始化，生成2lab_key.生成2lab_key.png两个文件。
2. 打开2lab_key.png，微信扫码即完成创建设计师个人站点，并且与当前comfyUI绑定。如果使用新的comfyUI环境，请再次微信扫码2lab_key.png，将会把你的账号重新绑定到最新的comfyUI环境。

## 模型标准化
由于服务器上的模型文件可能与你的comfyUI的模型文件位置不同，导致你设计的工作流无法在服务器上运行。因此，要求模型命名标准化，以huggingface和civitai上的模型命名为准。
开发者可以在本地的模型目录中建子目录管理模型，只要保持文件名不变，本插件的专用loader可以识别。
在modelSource目录中，列出了服务器支持的checkpoint、lora、vae和controlnet模型列表。如果开发者希望增加模型，可以与2lab联系，或者修改模型json文件后在github提交。

## 创作工作流
为了实现一键发布工作流，工作流中部分基础节点需要使用2lab的节点：
- checkpoint、lora、vae、controlnet的available loader只展示可用模型
- 允许最终用户输入的内容（例如图片），应使用2lab的InputText、InputSeed、InputImage节点，工作流发布到服务器时，服务器能自动将工作流转为小程序中的应用
- 工作流的最终输出，应使用2lab的outputText、outputImage节点
- 添加一个publish to 2lab节点，运行工作流时，该节点将把工作流发布到服务器，成为绘图模版。该节点默认publish字段设为false，改为true后才会发布工作流。

## 微信小程序
发布绘图模版后，在微信小程序"视觉工场2lab"中打开你的主页，可以查看你上传的绘图模版，以及作品。
绘图算力由小程序后端提供，绘图时会使用--disable-metadata参数启动comfyUI，因此生成的图片作品不会带工作流信息

# 限制
- 受限于算力，暂时不支持视频制作，但未来会支持
- 不支持调用本地大模型的节点，例如ComfyUI_VLM_nodes、comfyui-ollama
- 不支持use everywhere式无线连接，例如cg-use-everywhere
- 只支持本项目提供的模型列表，包括checkpoint、lora、vae、controlnet，清单在standardized目录中。如果希望增加支持的模型，可以在github中提交对standardized目录中的模型列表的修改，或者直接跟项目技术客服沟通）

# 模型下载

## 插件所需模型（自动下载）
本插件可以检查comfyUI中已经安装了哪些插件，并且检查需要的模型是否已经下载。如果没有下载，将会自动启动下载。此功能还在测试中，默认为关闭
下载模型有时会遇到网络问题，如果连接失败，可以重启comfyUI以继续采集。如果下载中断了，系统在下次下载时会自动断点续传

安装完本插件后第一次启动后，插件目录中会出现config.json
- auto_download_model代表是否自动安装插件所需要的模型文件到指定位置，默认为False
- china_mirror代表是否使用国内镜像下载模型，默认为True。当为True时，从hf-mirror.com下载模型；为False时，从huggingface.co下载模型。

目前已经支持自动模型的插件列表保存在standardized目录的model.json文件中，目前已经支持ComfyUI_IPAdapter_plus、ComfyUI_InstantID、PuLID_ComfyUI、ComfyUI-IC-Light、ComfyUI-SUPIR、ComfyUI-ELLA、ComfyUI-YoloWorld-EfficientSAM等插件

## checkpoint、lora、vae、controlnet模型（手动下载，未来将改为自动下载）
本项目使用的checkpoint、lora、vae、controlnet模型可以从下面的链接下载：
https://pan.baidu.com/s/1uJagXopHfEak1exT69gH9w?pwd=2lab

# 技术客服企业微信
![service](./asset/image/kefuQR.png)


