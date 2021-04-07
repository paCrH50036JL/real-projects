# coding=utf-8
'''
参考链接
https://stackoverflow.com/questions/10727131/why-is-tkinter-entrys-get-function-returning-nothing
https://jingyan.baidu.com/article/fb48e8be7bd73d2f622e14fd.html
https://jingyan.baidu.com/article/f54ae2fc6c29ec1e92b849cf.html
'''
import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # 窗口
        self.title('商标查找')
        self.geometry('500x300')
        self.resizable(width=False, height=False)
        # 输入框
        self.entry = tk.Entry(self)
        self.entry.place(relx=0.405, rely=0.5, anchor="center")
        # 按钮
        self.button = tk.Button(self, text="点击搜索", command=self.on_button)
        self.button.place(relx=0.7, rely=0.5, anchor="center")

    def on_button(self):
        # 点击按键打印输入内容
        print(self.entry.get())

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
