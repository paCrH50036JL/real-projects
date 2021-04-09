# coding=utf-8
'''
参考链接
https://stackoverflow.com/questions/10727131/why-is-tkinter-entrys-get-function-returning-nothing
https://jingyan.baidu.com/article/fb48e8be7bd73d2f622e14fd.html
https://jingyan.baidu.com/article/f54ae2fc6c29ec1e92b849cf.html
'''
import tkinter as tk
import datetime
tm_info = {'搜索网站': None, '商标信息': None}

# 设置Text框只允许打印不允许输入,参考
# https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only
def print2gui(content):
    global tm_info
    # 打印到界面
    text0.configure(state='normal')
    text0.insert(tk.END, content + '\n')
    if (tm_info['搜索网站'] != None) and (tm_info['商标信息'] != None):
        text0.insert(tk.END, tm_info)
        text0.insert(tk.END, '\n')
        tm_info = {'搜索网站': None, '商标信息': None}
    text0.configure(state='disabled')

def Button_callback():
    global tm_info
    # 获取当前输入
    content = text1.get(1.0, tk.END)
    print(content)
    # 清空输入框
    text1.delete(1.0, tk.END)
    # 输出内容到text0
    tm_info['商标信息'] = content.strip('\n')
    print2gui('\n商标信息:' + content)

def Button_all_callback():
    Checkbutton1.select()
    Checkbutton2.select()
    Checkbutton3.select()
    Checkbutton4.select()
    Checkbutton5.select()
    print2gui('已全部选中...')

def Button_none_callback():
    Checkbutton1.deselect()
    Checkbutton2.deselect()
    Checkbutton3.deselect()
    Checkbutton4.deselect()
    Checkbutton5.deselect()
    print2gui('已全部不选...')

def Checkbutton_callback():
    site = None
    global tm_info
    # 判断网址
    if var1.get() == 1:
        site = 'europa-eu'
    if var2.get() == 1:
        site = 'go-jp'
    if var3.get() == 1:
        site = 'gov-uk'
    if var4.get() == 1:
        site = 'uspto-gov'
    if var5.get() == 1:
        site = 'wipo-int'
    tm_info['搜索网站'] = site
    print2gui('\n搜索网站:' + site)

if __name__ == "__main__":
    window = tk.Tk()
    # 窗口
    window.title('商标查找')
    window.geometry('500x500')
    # 设置固定窗口大小,参考
    # https://stackoverflow.com/questions/37446710/how-to-make-a-tkinter-window-not-resizable
    window.resizable(width=False, height=False)
    # 复选框
    # 关于位置设置问题,详细参考
    # https://blog.csdn.net/zhang07083/article/details/103387798
    var1 = tk.IntVar()
    Checkbutton1 = tk.Checkbutton(window, text="europa-eu", variable=var1, onvalue=1, offvalue=0,\
                   command=Checkbutton_callback)
    Checkbutton1.place(x=0, y=0)
    var2 = tk.IntVar()
    Checkbutton2 = tk.Checkbutton(window, text="go-jp", variable=var2, onvalue=1, offvalue=0,\
                   command=Checkbutton_callback)
    Checkbutton2.place(x=100, y=0)
    var3 = tk.IntVar()
    Checkbutton3 = tk.Checkbutton(window, text="gov-uk", variable=var3, onvalue=1, offvalue=0, \
                   command=Checkbutton_callback)
    Checkbutton3.place(x=200, y=0)
    var4 = tk.IntVar()
    Checkbutton4 = tk.Checkbutton(window, text="uspto-gov", variable=var4, onvalue=1, offvalue=0, \
                   command=Checkbutton_callback)
    Checkbutton4.place(x=300, y=0)
    var5 = tk.IntVar()
    Checkbutton5 = tk.Checkbutton(window, text="wipo-int", variable=var5, onvalue=1, offvalue=0, \
                   command=Checkbutton_callback)
    Checkbutton5.place(x=400, y=0)
    var_all = tk.IntVar()
    # Checkbutton_all = tk.Checkbutton(window, text="选中所有", variable=var_all, onvalue=1, offvalue=0, \
    #                command=Checkbutton_callback)
    # Checkbutton_all.place(x=100, y=25)
    # var_none = tk.IntVar()
    # Checkbutton_none = tk.Checkbutton(window, text="全都不选", variable=var_none, onvalue=1, offvalue=0, \
    #                command=Checkbutton_callback)
    # Checkbutton_none.place(x=300, y=25)
    # 打印框
    text0 = tk.Text(window, width=100, height=25, state=tk.DISABLED)
    text0.place(x=0, y=250)
    # 输入框
    text1 = tk.Text(window, width=25, height=10)
    text1.place(x=125, y=80)
    # 按钮
    button = tk.Button(window, text="点击搜索", command=Button_callback)
    button.place(x=350, y=125, anchor="center")
    button_all = tk.Button(window, text="全部选中", command=Button_all_callback)
    button_all.place(x=130, y=50, anchor="center")
    button_none = tk.Button(window, text="全部不选", command=Button_none_callback)
    button_none.place(x=300, y=50, anchor="center")
    # 循环等待
    window.mainloop()
