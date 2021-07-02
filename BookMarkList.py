import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from typing import NoReturn

# 格式化時間
def mark_time(line):
    mark_lindex = line.find("=")
    mark_rindex = line.find("*")
    mark_timeN = line[mark_lindex+1:mark_rindex]  # 取得時間敘述
    #格式化時間
    while len(mark_timeN)<9:
        mark_timeN = "0" + mark_timeN
    mark_time = "[{0}:{1}:{2}.{3}]".format(mark_timeN[:2], mark_timeN[2:4], mark_timeN[4:6], mark_timeN[6:])
    return mark_time

# 取得書籤標題
def mark_title(line):
    lindex = line.find("*")  # 取得左邊第一個 * 的 index
    rindex = line.rfind("*")   # 取得右邊邊第一個 * 的 index
    mark_title = line[lindex+1:rindex]   # 取得文字內容
    return str(mark_title)

# 將書籤內容整理成 md 檔
def make_md_list(data_path):
    if msgbox("makelist"):
        return None
    with filedialog.asksaveasfile(title="儲存檔案", mode="w", defaultextension=".md", filetypes=[("Markdown File","*.md")]) as bml:
        folder_name = ""
        for path in data_path:
            # 取得路徑中各檔案名稱
            path_split = path.split("/")
            # 判斷資料夾名稱是否相同 不同：寫入資料夾名稱、相同不寫入
            if folder_name != path_split[-2]:
                bml.write("## 資料夾： " + path_split[-2] + "\n")
                folder_name = path_split[-2]
            # 開啟目標檔案
            with open(path, "r", encoding="utf-16LE") as f:
                # 寫入檔案名稱
                bml.write("### 檔案名稱： "+ path_split[-1][:-4]+ "\n")
                #  readlines() 方法將檔案內容按新行分割成一個列表返回
                lines = f.readlines()
                # 遍歷
                count = 0
                for line in lines:
                    if "*" in line:
                        mark_times = mark_time(line)
                        mark_titles = mark_title(line)
                        count += 1  # 書籤編號
                        # print(mark_times + " " + mark_titles)
                        bml.write(str(count)+ ". "+ mark_times+ " -- "+ mark_titles+ "\n")  # 寫入 md 檔
                bml.write("---\n")
            write_progressbar(data_path)

# 將書籤內容整理成 text 檔
def make_txt_list(data_path):
    if msgbox("makelist"):
        return None
    with filedialog.asksaveasfile(title="儲存檔案", mode="w", defaultextension=".text", filetypes=[("文字文件","*.txt")]) as bml:
        folder_name = ""
        for path in data_path:
            # 取得路徑中各檔案名稱
            path_split = path.split("/")
            # 判斷資料夾名稱是否相同 不同：寫入資料夾名稱、相同不寫入
            if folder_name != path_split[-2]:
                bml.write("資料夾： " + path_split[-2] + "\n")
                folder_name = path_split[-2]
            # 開啟目標檔案
            with open(path, "r", encoding="utf-16LE") as f:
                # 寫入檔案名稱
                path_lindex = path.rfind("/")
                path_rindex = path.rfind(".")
                print(path_lindex)
                bml.write("     ---檔案名稱： "+ path[path_lindex+1:path_rindex]+ "---\n")
                #  readlines() 方法將檔案內容按新行分割成一個列表返回
                lines = f.readlines()
                # 遍歷
                count = 0
                for line in lines:
                    if "*" in line:
                        mark_times = mark_time(line)
                        mark_titles = mark_title(line)
                        count += 1  # 書籤編號
                        print(mark_times + " " + mark_titles)
                        bml.write("     " + str(count)+ ". "+ mark_times+ " "+ mark_titles+ "\n")  # 寫入 txt 檔
                bml.write("\n")
            global write_times
            write_times += 1
            file_progressbar["value"] = write_times
            root.update()

# 顯示選擇的檔案
def show_list(path):
    global list_count
    # 顯示到 file_list Listbox 上
    file_list.insert("end","[{0}] {1}".format(list_count, path))
    list_count += 1
    Yaxis_scrollbar.config(command=file_list.yview)
    Xaxis_scrollbar.config(command=file_list.xview)
    return None

# 按鈕功能：搜尋檔案
def file_select():
    global data_path
    paths = filedialog.askopenfilenames(title="選擇書籤檔案",
                                          filetype=(("PotPlayer 書籤檔案", "*.pbf"),("All Files", "*.*")))
    for path in paths:
        data_path.append(path)
        show_list(path)  # 顯示選擇的檔案
    return None

#按鈕功能：搜尋資料夾內所有.pbf檔案
def folder_select():
    global data_path
    paths = filedialog.askdirectory(title="選擇資料夾")
    for root, dirs, files in os.walk(paths):
        for file_name in files:
            if file_name.endswith(".pbf"):
                path = os.path.join(root, file_name).replace("\\","/")
                data_path.append(path)
                show_list(path)

# 按鈕功能：移除檔案
def file_delete(deAll = False):
    global data_path
    global list_count
    list_count = 1
    if msgbox("isdelete"):
        # 移除全部檔案
        if deAll:
            del data_path[0:]
            file_list.delete(0, "end")   # 清除 List
            return None
        # 移除選定檔案
        indexs = list(file_list.curselection())
        del data_path[indexs[0]]  # 先移除 indexs 中第一個
            # 迭代移除
        delete_count = 1
        for index in indexs[1:]:   
            del data_path[index-delete_count]   # 每刪除一次索引需-1
            delete_count += 1
            # 重新顯示 Lsit
        file_list.delete(0, "end")   # 清除 List
        for path in data_path:
            show_list(path)
        return None
    return None

# 建立進度條
def write_progressbar(data_path):
    global write_times
    file_progressbar["maximum"] = len(data_path)
    write_times += 1
    file_progressbar["value"] = write_times
    root.update()
    return None

# 建立對話框
def msgbox(info, e=None):
    global data_path
    # 對話框-刪除功能 return False -> 不執行
    if info == "isdelete":
        if data_path == []:
            messagebox.showerror("移除檔案", "未選擇檔案")
            return False
        return messagebox.askokcancel("移除檔案", "將移除所選取的檔案，實際檔案不會刪除\n是否執行?")
    # 對話框-輸出功能  return Ture -> 不執行
    elif info == "makelist":
        if data_path == []:
            messagebox.showerror("儲存檔案", "未選擇檔案")
            return True
        return False
    # 對話框-離開功能
    elif info == "exit":
        if messagebox.askyesno("離開程式", "確定要離開程式?"):
            root.destroy()
        else:
            return None
    # 對話框-異常處理資訊
    elif info == "exception":
        messagebox.showwarning("異常資訊", e)

# 建立GUI
root = tk.Tk()
root.title("影片書籤統整系統")
root.geometry("480x310")
root.resizable(False, False)   # 固定視窗大小
try:
    root.iconbitmap("logo.ico")
except Exception as i:
    e = str(i) + "\n請將\"logo.ico\"檔案放置相同資料夾 "
    msgbox("exception", e)
    
data_path = []  # 紀錄選擇的檔案
list_count = 1  # 計算列表列號
write_times = 0

# 建立 ListBox 外框
labelFrame = tk.LabelFrame(root, text="已選擇的檔案", height=10)
labelFrame.pack(fill="x")
    # 建立 X,Y 卷軸
Yaxis_scrollbar = tk.Scrollbar(labelFrame, orient="vertical")
Yaxis_scrollbar.pack(side="right", fill="y")
Xaxis_scrollbar = tk.Scrollbar(labelFrame, orient="horizontal")
Xaxis_scrollbar.pack(side="bottom", fill="x")
    # 建立 ListBox
file_list = tk.Listbox(labelFrame, height=10,yscrollcommand=Yaxis_scrollbar.set, xscrollcommand=Xaxis_scrollbar.set, 
                        selectmode="extended")
file_list.pack(fill="x", expand="True")

# 建立按鈕區外框
button_Frame = tk.LabelFrame(root, relief="flat")
button_Frame.pack(fill="x")
butten_packs = {"side":"left", "padx":"5"}
    # 右邊按鈕
button_r_Frame = tk.LabelFrame(button_Frame, relief="flat")
button_r_Frame.pack(side="right", fill="both", expand=True)
butten_exit = tk.Button(button_r_Frame, width=12, text="關閉程式",command=lambda:msgbox("exit"))
butten_exit.pack(side="left", fill="y")
    # 上層按鈕
button_up_Frame = tk.LabelFrame(button_Frame, relief="flat")
button_up_Frame.pack(padx=10, fill="x")
button_choice = tk.Button(button_up_Frame, text="選擇書籤檔案", width=12, command=lambda:file_select())
button_choice.pack(butten_packs)
button_delete = tk.Button(button_up_Frame, width=12, text="移除檔案", command=lambda:file_delete())
button_delete.pack(butten_packs)
button_save_md = tk.Button(button_up_Frame, width=12, text="儲存為 md 檔", command=lambda:make_md_list(data_path))
button_save_md.pack(butten_packs)
    # 下層按鈕
button_dw_Frame = tk.LabelFrame(button_Frame, relief="flat")
button_dw_Frame.pack(padx=10, fill="x")
button_folder = tk.Button(button_dw_Frame, width=12, text="搜尋資料夾", command=lambda:folder_select())
button_folder.pack(butten_packs)
button_delete_all = tk.Button(button_dw_Frame, width=12, text="移除全部檔案", command=lambda:file_delete(deAll=True))
button_delete_all.pack(butten_packs)
button_save_txt = tk.Button(button_dw_Frame, width=12, text="儲存為純文字檔",command=lambda:make_txt_list(data_path))
button_save_txt.pack(butten_packs)

# 建立進度條
progressbarFrame = tk.LabelFrame(root, relief="sunken")
progressbarFrame.pack(padx=10, pady=10, fill="x")
file_progressbar = ttk.Progressbar(progressbarFrame, mode="determinate", length=450)
file_progressbar["value"] = 0
file_progressbar.pack()

root.mainloop()
