import random
import tkinter as tk


def show_warming(tim):
    def foo():
        nonlocal tim
        tim -= 1
        time_lable['text'] = str(tim) + "救命", "太吵了没法睡觉了啊！"
        # root1['bg'] = random.choice(['blue', 'green', 'yellow', 'pink'])
        mycolor = '#%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # set your favourite rgb color
        root1.configure(bg=mycolor)
        time_lable.place(relx=random.uniform(0, 0.5), rely=random.uniform(0, 0.9))
        time_lable.after(1000, foo)

    root1 = tk.Tk()
    root1.attributes('-fullscreen', True)
    root1.attributes('-topmost', True)
    time_lable = tk.Label(root1, text=str(tim) + "救命, 太吵了没法睡觉了啊！", font=('Arial', 48), bg='white')

    time_lable.place(relx=0.01, rely=0.2)
    time_lable.after(1000, foo)  # 每1000毫秒调用一次foo

    root1.after(tim * 1000, root1.destroy)
    root1.mainloop()
