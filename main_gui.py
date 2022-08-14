import logging
import tkinter as tk

import global_var
from global_var import Flags
from main import print_hi, update_config, init_config
from tkSliderWidget import Slider


def btn1_only_once(e):
    if Flags.runningFlag:
        logging.info('已经在运行了')
    else:
        Flags.runningFlag = True
        check_current_remain_sec()
        print_hi()


def set_db_threshold(e):
    Flags.dbThres = scale.get()


init_config()

root = tk.Tk()
root.title('修普诺斯守护神')
root.geometry("520x321+550+150")
# 创建按钮，并且将按钮放到窗口里面
btn1 = tk.Button(root)
btn1["text"] = "开始守护"  # 给按钮一个名称
btn1.bind("<Button-1>", btn1_only_once)  # 将按钮和方法进行绑定，也就是创建了一个事件
btn1.grid(row=0, column=0)  # 按钮布局

# 敏感度（相对db阈值）
label = tk.Label(root, text='友好提醒相对db阈值（敏感度）：')
label.grid(row=2, column=0)

scale = tk.Scale(root, from_=5, to=30, orient=tk.HORIZONTAL,
                 command=set_db_threshold, tickinterval=5, length=200)
scale.set(Flags.dbThres)
scale.grid(row=2, column=1)

# 检测环境音 3s
remain_sec = global_var.check_surroundings_db_second


def check_current_remain_sec():
    global remain_sec
    remain_sec -= 1
    label['text'] = '检测环境音量中，剩余{}s'.format(remain_sec)

    if remain_sec > 0:
        label.after(1000, check_current_remain_sec)
    else:
        label['text'] = '环境音量检测完成~'
        remain_sec = global_var.check_surroundings_db_second


label = tk.Label(root, text='待检测当前环境音量')
label.grid(row=1, column=0)


# 状态指示灯, 0.5s检测一次。同时也是定时的巡检
def change_state_color():
    if Flags.runningFlag:
        canvas.itemconfigure('status', fill='green')
    else:
        canvas.itemconfigure('status', fill='red')
        label['text'] = '待检测当前环境音量'
    global_var.HearFrequency.lowFre, global_var.HearFrequency.highFre = slider.getValues()
    canvas.after(500, change_state_color)


label2 = tk.Label(root, text='设置声音频率响应范围Hz')
label2.grid(row=4, column=0)
slider = Slider(
    root,
    width=300,
    height=60,
    min_val=20,
    max_val=20000,
    init_lis=[global_var.HearFrequency.lowFre, global_var.HearFrequency.highFre],
    show_value=True,
    removable=True,
    addable=False,
)
slider.grid(row=4, column=1)

label1 = tk.Label(root, text='运行状态：')
label1.grid(row=5, column=0)

canvas = tk.Canvas(root, width=50, height=50, borderwidth=0, highlightthickness=0)
center_of_circle = (25, 25)
radium_of_circle = 15
canvas.create_oval(center_of_circle[0] - radium_of_circle, center_of_circle[1] - radium_of_circle,
                   center_of_circle[0] + radium_of_circle, center_of_circle[1] + radium_of_circle,
                   fill="red", tags='status')
canvas.grid(row=5, column=1)
canvas.after(500, change_state_color)

btn2 = tk.Button(root, text="保存当前个性化设置", command=update_config)
btn2.grid(row=6, column=0)  # 按钮布局

root.mainloop()
