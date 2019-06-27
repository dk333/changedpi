import os
import sys
import time
import tkinter
import tkinter.messagebox
from multiprocessing.dummy import Pool

from PIL import Image

global PATH, DPI, QCOMPRESS


def get_files(path):
    """递归获取指定类型的文件"""
    ext0 = ".jpeg"
    ext1 = ".jpg"
    pre = "~"
    files = []
    for dirpath, dirnames, fnames in os.walk(path):
        for fname in fnames:
            fn = fname.lower()
            start = fn.startswith(pre)
            end = fn.endswith(ext0) or fn.endswith(ext1)
            fullname = os.path.join(dirpath, fname)
            if not start and end:
                files.append(fullname)
    return files


def doJob():
    global PATH, DPI, QCOMPRESS
    t1 = time.time()
    q = int(QCOMPRESS.get().strip())
    dpi = int(DPI.get().strip())

    def fun(filename):
        print(filename)
        Image.open(filename).save(filename, dpi=(dpi, dpi), optimize=True, quality=q)

    path = PATH.get(1.0, 2.0).strip()
    print(path)
    files = get_files(path)
    pool = Pool()
    a = pool.map(fun, files)
    pool.close()
    pool.join()
    total = len(files)
    passtime = round(time.time()-t1, 2)
    speed = total/passtime
    msg = "文件个数: %s 个, 用时 %s 秒, 速度 %0.2f 个/秒" % (total, passtime, speed)
    tkinter.messagebox.showinfo("完成", msg)


def main():
    global PATH, DPI, QCOMPRESS
    window = tkinter.Tk()
    window.title("调整图片工具")
    window.geometry("480x240+500+255")
    tkinter.Button(window, text="执行", command=doJob).pack()

    L = tkinter.Label(window, text="DPI").pack()
    DPI = tkinter.Entry(window)
    DPI.insert(0, 300)
    DPI.pack()

    tkinter.Label(window, text="压缩率(1~100), 数字越大品质越好").pack()
    QCOMPRESS = tkinter.Entry(window, text="DPI")
    QCOMPRESS.insert(0, 30)
    QCOMPRESS.pack()

    tkinter.Label(window, text="图片路径").pack()
    path = r""

    PATH = tkinter.Text(window, width=200)
    PATH.insert(1.0, path)
    PATH.pack()
    window.mainloop()


if __name__ == '__main__':
    main()
