import os
import random
import hashlib

ip_list = {
    '芜湖区':'192.168.0.91',
    '北京A区':'100.72.64.19',
    '内蒙A区':'192.168.1.174',
    '泉州A区':'10.55.146.88',
    '南京新手区':'172.181.217.43',
    '佛山区':'192.168.126.12',
    '北京C区':'172.31.1.127',
    '宿迁区':'10.0.0.7',
    '内蒙B区':'192.168.1.174',
}

def get_speed_ip():
    for item in ip_list:
        print(item)
        if(os.system(f'ping -c 1 -w 1 {ip_list[item]}') == 0):
            return [item,ip_list[item]]
    return '-1'

def get_is_speed():
    return os.getenv("http_proxy") != None

def get_have_aria2():
    return os.system(f'aria2c -v') == 0

embeddings_dir_1 = "/embeddings"
hypernetworks_dir_2 = "/models/hypernetworks"
ckpt_dir_3 = "/models/Stable-diffusion"

def get_sd_dir():
    if os.path.exists("/root/stable-diffusion-webui"):
        return "/root/stable-diffusion-webui"
    elif os.path.exists("/root/autodl-tmp/stable-diffusion-webui"):
        return "/root/autodl-tmp/stable-diffusion-webui"
    else:
        return "-1"
    
def get_download_dir(style):
    sd_dir = get_sd_dir()
    mv_dir = "-1"
    if sd_dir != "-1":
        if style == 1:
            mv_dir = sd_dir + embeddings_dir_1
        if style == 2:
            mv_dir = sd_dir + hypernetworks_dir_2
        if style == 3:
            mv_dir = sd_dir + ckpt_dir_3
        if style == 4:
            mv_dir = "/root/autodl-tmp/"
        return mv_dir
    else:
        return "-1"
        
def get_download_command(url,style):
    download_dir = get_download_dir(style)
    if download_dir != "-1":
        command = "cd " + download_dir + " && aria2c -s 16 -x 8 --seed-time=0 '" + url + "' && echo 下载完毕!文件已保存到" + download_dir
        return command
    else:
        return "echo 未找到目录!无法下载!"

def generate_random_str(randomlength = 8):
    random_str = ''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) -1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def model_hash(filename):
    try:
        with open(filename, "rb") as file:
            import hashlib
            m = hashlib.sha256()

            file.seek(0x100000)
            m.update(file.read(0x10000))
            return m.hexdigest()[0:8]
    except FileNotFoundError:
        return 'NOFILE'
    
def get_style_mod_dir(style):
    sd_dir = get_sd_dir()
    mv_dir = "-1"
    
    if style == 1:
        mv_dir = sd_dir + embeddings_dir_1
    if style == 2:
        mv_dir = sd_dir + hypernetworks_dir_2
    if style == 3:
        mv_dir = sd_dir + ckpt_dir_3
    
    return mv_dir
    
def scan_dir_hash(style):
    mod_dir = get_style_mod_dir(style)
    hash_list = []
    for file_name in os.listdir(mod_dir):
        file_dir = mod_dir + "/" + file_name
        if os.path.isfile(file_dir):
            hash_list.append(model_hash(file_dir))
    return hash_list