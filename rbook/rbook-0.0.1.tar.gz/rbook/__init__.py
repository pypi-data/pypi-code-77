from tkinter import *
import tkinter.ttk as tsk
from tkinter.messagebox import *


def book(pages, index=0, wintitle="Book"):
    class Iv():
        v = index

    V = Iv()
    tk = Tk()
    tk.resizable(0, 0)
    tk.title(wintitle)
    t = Text(tk)
    t.pack()
    t.insert(END, pages[V.v])

    show = Label(tk, text=str(V.v + 1) + "/" + str(len(pages)))
    show.pack()

    def nxtp():
        V.v = V.v + 1
        t.delete("1.0", "end")
        try:
            t.insert(END, pages[V.v])
            show.config(text=str(V.v + 1) + "/" + str(len(pages)))
        except IndexError:
            showerror("超页", "后面没有了，去前面看看吧！")
            V.v = -1
            nxtp()

    def lstp():
        V.v = V.v - 1
        t.delete("1.0", "end")
        if V.v < 0:
            showerror("超页", "前面没有了，去后面看看吧！")
            V.v = 1
            lstp()
            return
        t.insert(END, pages[V.v])
        show.config(text=str(V.v + 1) + "/" + str(len(pages)))

    def top(e):
        pnum = pn.get()
        pnum = int(pnum)
        if pnum < 1 or pnum > len(pages):
            showerror("不存在", "此页面不存在！")
            return
        V.v = pnum - 2
        nxtp()

    nxt = tsk.Button(tk, text="下一页", command=nxtp)
    nxt.pack(fill=X)
    lst = tsk.Button(tk, text="上一页", command=lstp)
    lst.pack(fill=X)
    Label(tk, text="跳转至").pack(side="left", pady=5)
    pn = tsk.Entry(tk, width=5)
    pn.pack(side="left", pady=5)
    pn.bind("<Return>", top)


def srt():
    mainloop()


if __name__ == "__main__":
    p1 = "作者：郭燕铭"
    p2 = "库名：NewBook"
    p3 = "使用插件：Tkinter"
    p4 = "学而思个人主页：https://code.xueersi.com/space/21914411"
    p5 = "快使用NewBook创造你的故事传奇吧！"
    book([p1, p2, p3, p4, p5], wintitle="简介：", index=4)
    srt()
