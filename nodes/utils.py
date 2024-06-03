import os.path
import subprocess
import traceback
import qrcode
from PIL import Image
from .constants import project_root, models, custom_nodes_root, comfyUI_models_root, config


def auto_download_model():
    custom_nodes_dirs = [name for name in os.listdir(custom_nodes_root) if os.path.isdir(os.path.join(custom_nodes_root, name)) and name != '__pycache__']

    # check nodes to download
    for key,value in models.items():
        if key in custom_nodes_dirs:
            print(f"start download model file for {key}")
            for file in value['models']['files']:
                url = file['url']
                save_path = file['save_path']
                filename = file['filename']
                save_full_path = os.path.join(comfyUI_models_root,save_path)
                file_path = os.path.join(save_full_path,filename)
                if os.path.exists(file_path):
                    print(f"{file_path} already exists")
                    continue
                if not os.path.exists(save_full_path):
                    os.makedirs(save_full_path)
                if config['china_mirror']:
                    # huggingface 换成国内镜像站
                    if url.startswith('https://huggingface.co/'):
                        url = url.replace('https://huggingface.co/', 'https://hf-mirror.com/')
                if url.startswith('https://huggingface.co/') or url.startswith('https://hf-mirror.com/'):
                    success = download_huggingface_model(url,save_full_path,filename)
                    if success=='KeyboardInterrupt':
                        print_error("Keyboard Interrupt")
                        break
                    elif success=='fail':
                        print_error("download failed : "+url)
                        continue
                else:
                    print("unsuppoted url : ",url)
                    continue
def download_huggingface_model(url, save_full_path, filename) ->str:
    try:
        tempfilename = filename+".temp"
        temp_file_path = os.path.join(save_full_path, tempfilename)
        file_path = os.path.join(save_full_path,filename)

        wget_command = [
            'wget',
            '-c',
            '-O', temp_file_path,
            url
        ]
        # print("wget command : ",wget_command)
        wget_process = subprocess.run(wget_command, check=True)

        # 构建修改文件名的命令
        rename_command = [
            'mv',
            temp_file_path,
            file_path
        ]
        rename_process = subprocess.run(rename_command, check=True)

        # run unzip for zip file
        if filename.endswith('.zip'):
            unzip_command = ['unzip', file_path, '-d', save_full_path]
            unzip_process = subprocess.run(unzip_command, check=True)

        return 'success'
    except KeyboardInterrupt:
        print("命令执行被用户中断。")
        return 'KeyboardInterrupt'
    except subprocess.TimeoutExpired:
        print("命令执行超时。")
        return 'Fail'
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，退出码：{e.returncode}")
        print(f"输出：{e.output}")
        print(f"错误输出：{e.stderr}")
        return 'Fail'
    except:
        print(traceback.format_exc())
        return 'Fail'


def execute_command(command, working_dir)->bool:
    try:
        # 执行Git命令
        print("execute_command : ",command)
        output = subprocess.run(command, cwd=working_dir, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
        print(output.stdout)
        # print(output.decode('utf-8').strip())
        return True
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，打印错误信息
        print(f"Git command failed with error: {e.output.decode('utf-8').strip()}")
        return False

def create_qr_code(url, file_path='2lab_key.png'):
    try:
        # 指定二维码的宽度像素
        qr_width_pixels = 600

        # 计算box_size参数，它是每个小方块的像素大小
        # 假设你想要二维码的宽度为300像素，那么每个小方块的像素大小就是300 / 21（版本1的二维码大小）
        # 这里我们使用版本1的二维码，因为它是21x21的方块
        box_size = qr_width_pixels // 21
        print(f"box_size: {box_size} pixels")

        # 创建二维码实例
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=2,
        )

        # 添加数据
        qr.add_data(url)
        qr.make(fit=True)

        # 创建二维码图片
        img_qr = qr.make_image(fill_color="black", back_color="white")
        img_qr = img_qr.convert("RGBA")  # 添加这一行来进行模式转换
        img_qr = img_qr.resize((800, 800))

        # 创建一个新的图片，用于添加文字
        width_qr, height_qr = img_qr.size
        asset_path = os.path.join(project_root, 'asset')
        asset_image_path = os.path.join(asset_path, 'image')
        text_image_path = os.path.join(asset_image_path, 'scantext.png')

        with Image.open(text_image_path) as text_image:
            # 确保text_image以RGBA模式打开
            text_image = text_image.convert('RGBA')

            # 获取图片的宽度和高度
            width_text, height_text = text_image.size

            # 计算图片B的新宽度（A宽度的3/4）和新高度（基于宽度）
            new_width_text = int(width_qr * 3 / 4)
            new_height_text = int(new_width_text * height_text / width_text)
            text_image_new = text_image.resize((new_width_text, new_height_text))
            width_text, height_text = text_image_new.size

            background_color = "white"  # 背景色为纯白色

            # 创建一张新的图片，颜色设定为白色
            width_bg = width_qr
            height_bg = height_qr + height_text + int(height_qr / 20)
            background = Image.new('RGB', (width_qr, height_bg), background_color)
            print(f"background width: {width_bg} pixels")
            print(f"background height: {height_bg} pixels")

            # 在新的图片中嵌入QR码
            background.paste(img_qr, (0, 0))
            background.paste(text_image_new, (int(width_qr / 8), height_qr), text_image_new)

            background.save(file_path)

    except:
        print(traceback.format_exc())

def truncate_string(s):
    # 查找 "/" 或 "\" 最后一次出现的位置
    index = max(s.rfind('/'), s.rfind('\\'))
    # 如果找到了至少一个分隔符，则截断字符串
    if index != -1:
        return s[index + 1:]  # 保留分隔符之后的部分
    else:
        return s  # 如果没有找到分隔符，返回原字符串

def filter_list(origin_list, filter_list):
    map = {}
    for item in origin_list:
        key = truncate_string(item)
        value = item
        map[key] = value

    filtered_list = []
    for key, value in map.items():
        if key in filter_list:
            filtered_list.append(value)
    return filtered_list


def print_console(text):
    print(f"\033[36m{text}\033[0m")
def print_error(text):
    print(f"\033[31m{text}\033[0m")