import tkinter as tk
import subprocess
import socket
import shelve
import sys

root = tk.Tk()
root.title("Flask")
root.geometry("260x140")

text = tk.Label(root, text="伺服器未啟動", font=("Arial", 13, "bold"), fg="red")
text.place(x=0, y=35)

server_process = None 

#拿資料
def finds():
    with shelve.open("patie") as file:
        if "list" not in file or not file["list"]:
            file["list"] = {'tom':{'age':25,'id':1}, 'yoyo':{'age':11,'id':2}}
        lists = file["list"]
        keys = list(lists.keys())
        print(lists)
    return lists, keys

lists, keys = finds()

def againlist():
    global lists, keys
    lists, keys = finds()
    drop["menu"].delete(0, "end")
    if lists:
        var.set(keys[0])
        for i in keys:
            drop["menu"].add_command(label=i, command=tk._setit(var, i))
    else:
        var.set("無")
        drop["menu"].add_command(label="無", command=tk._setit(var, "無"))

def news():
    text=enter.get().strip()
    scr=ages.get().strip()
    if vars.get()=='使用者':
        with shelve.open("patie", writeback=True) as file:
            if not text in file['list'] and text!='' and scr!='':
                file["list"][text]={'age':scr,'id':len(file["list"])}
                file.sync()
                againlist()
    else:
        with shelve.open("patie", writeback=True) as file:
            if not text in file['list'] and text!='':
                file["list"][text]={'cmd':True,'id':len(file["list"])}
                file.sync()
                againlist()

def dele():
    key = var.get()
    with shelve.open("patie", writeback=True) as file:
        if key in file["list"]:
            del file["list"][key]
            file.sync()
    againlist()

var = tk.StringVar(value=keys[0] if keys else "無")
drop = tk.OptionMenu(root, var, *keys)
drop.place(x=130, y=98)

#檢查伺服器 
def flas(t=0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1)
        s.connect(("127.0.0.1", 5000))
        s.close()
        if t == 0:
            text.config(text="伺服器已啟動", fg="green")
        else:
            return True
    except:
        if t == 0:
            text.config(text="伺服器未啟動", fg="red")
        else:
            return False

flas()

#開/關伺服器 
def op():
    global server_process

    if server_process and server_process.poll() is None:
        # 已啟動關掉
        server_process.terminate()  #結束
        try:
            server_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_process.kill()  # 強制
        server_process = None
        text.config(text="伺服器已關閉", fg="red")
    else:
        # 開啟伺服器
        server_process = subprocess.Popen(
            [sys.executable, r"c:\Users\kauhou\OneDrive\桌面\car python\搜尋使用者\hava.py"]
        )
        text.config(text="伺服器已啟動", fg="green")

# ------------------- Tkinter 按鈕 -------------------
no=["使用者","管理者"]
vars = tk.StringVar(value=no[0] if keys else "無")
drops = tk.OptionMenu(root, vars, *no)
drops.place(x=127, y=12)

tk.Button(root, text="刪除", command=dele).place(x=200, y=100)
tk.Button(root, text="開/關伺服器", command=op).place(x=20, y=90)
tk.Button(root, text="新增", command=news).place(x=215, y=40)
enter=tk.Entry(root,width=10)
enter.place(x=130,y=40)
ages=tk.Entry(root,width=10)
ages.place(x=130,y=60)

root.mainloop()
