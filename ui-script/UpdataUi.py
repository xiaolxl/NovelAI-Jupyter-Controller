import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import os

import Utils

def getUi(data,cmd_run):
    out = widgets.Output(layout={'border': '1px solid black'})
    
    updata_tip = widgets.HTML(
        value="<p><font color='#e800e0'>非必要不更新,启动器与汉化插件除外</font></p><p><font color='#e800e0'>更新前记得开学术加速</font></p>",
    )
    
    # ====================
    
    updata_controller_buttom = widgets.Button(
            description='更新启动器(注意这是强制覆盖)',
            style={'description_width': 'initial'},
            layout=Layout(width='300px', height='auto'),
            button_style='primary'
    )
    
    updata_webui_buttom = widgets.Button(
            description='更新WebUi',
            button_style='success'
    )
    
    updata_db_buttom = widgets.Button(
        description='更新DreamBooth',
        button_style='success'
    )
    
    updata_chinese_buttom = widgets.Button(
        description='更新汉化插件',
        button_style='success'
    )

    #运行函数
    def run_click(index):
        out.clear_output()
        with out:
            temp = False
            sd_dir = Utils.get_sd_dir()

            if sd_dir == "-1":
                print("无法找到程序目录")
            else:
                head = "echo 正在更新，请稍等... && "
                tail = " && echo 更新完成!"
                if index == 0:
                    cmd_run(head + "cd /root/NovelAI-Jupyter-Controller && git fetch --all && git reset --hard origin && git pull" + tail + " && echo 请重启所有内核并关闭所有窗口重新打开")
                if index == 1:
                    cmd_run(head + "cd " + sd_dir + " && git pull" + tail)

                if index == 2:
                    cmd_run(head + "cd " + sd_dir + "/extensions/sd_dreambooth_extension" + " && git pull" + tail)

                if index == 3:
                    cmd_run(head + "cd " + sd_dir + "/extensions/stable-diffusion-webui-localization-zh_CN" + " && git pull" + tail)
    
    def updata_controller_buttom_(self):
        run_click(0)   
    
    def updata_webui_buttom_(self):
        run_click(1)

    def updata_db_buttom_(self):
        run_click(2)
    
    def updata_chinese_buttom_(self):
        run_click(3)
    
    #绑定加速函数
    updata_controller_buttom.on_click(updata_controller_buttom_)
    updata_webui_buttom.on_click(updata_webui_buttom_)
    updata_db_buttom.on_click(updata_db_buttom_)
    updata_chinese_buttom.on_click(updata_chinese_buttom_)
    
    return VBox([updata_tip,updata_controller_buttom,updata_webui_buttom,updata_db_buttom,updata_chinese_buttom,out])