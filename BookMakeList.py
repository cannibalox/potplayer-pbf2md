import tkinter as tk
from tkinter import filedialog, messagebox, ttk


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
    with filedialog.asksaveasfile(title="儲存檔案", mode="w", defaultextension=".md", filetypes=[("Markdown File","*.md")]) as bml:
        for path in data_path:
            # 開啟目標檔案
            with open(path, "r", encoding="utf-16LE") as f:
                # 寫入檔案名稱
                path_lindex = path.rfind("/")
                path_rindex = path.rfind(".")
                bml.write("## 檔案名稱： "+ path[path_lindex+1:path_rindex]+ "\n")
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
                        bml.write(str(count)+ ". "+ mark_times+ " -- "+ mark_titles+ "\n")  # 寫入 md 檔
                bml.write("---\n")

# 將書籤內容整理成 text 檔
def make_txt_list(data_path):
    with filedialog.asksaveasfile(title="儲存檔案", mode="w", defaultextension=".text", filetypes=[("文字文件","*.txt")]) as bml:
        for path in data_path:
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
                        bml.write(" " + str(count)+ ". "+ mark_times+ " "+ mark_titles+ "\n")  # 寫入 txt 檔
                bml.write("\n")

# 顯示選擇的檔案
def show_list(list):
    global list_count
    # 顯示到 file_list Listbox 上
    file_list.insert("end","[{0}] {1}".format(list_count, list))
    list_count += 1
    Yaxis_scrollbar.config(command=file_list.yview)
    Xaxis_scrollbar.config(command=file_list.xview)
    return None

# 按鈕功能：搜尋檔案
def File_dialog():
    global data_path
    paths = filedialog.askopenfilenames(title="選擇書籤檔案",
                                          filetype=(("PotPlayer 書籤檔案", "*.pbf"),("All Files", "*.*")))
    for path in paths:
        data_path.append(path)
        show_list(path)  # 顯示選擇的檔案
    return None


# 建立GUI
root = tk.Tk()
root.title("影片書籤統整系統")
root.geometry("500x300")
root.resizable(False, False)   # 固定視窗大小
data_path = []  # 紀錄選擇的檔案
list_count = 1  # 計算列表列號

# 建立 外框
labelFrame = tk.LabelFrame(root, text="已選擇的檔案", height=10)
labelFrame.pack(fill="x")
# 建立 X,Y 卷軸
Yaxis_scrollbar = tk.Scrollbar(labelFrame, orient="vertical")
Yaxis_scrollbar.pack(side="right", fill="y")
Xaxis_scrollbar = tk.Scrollbar(labelFrame, orient="horizontal")
Xaxis_scrollbar.pack(side="bottom", fill="x")
# 建立 ListBox
file_list = tk.Listbox(labelFrame, height=10,yscrollcommand=Yaxis_scrollbar.set, xscrollcommand=Xaxis_scrollbar.set)
file_list.pack(fill="x", expand="True")

# 建立按鈕
buttonFrame = tk.LabelFrame(root, height=10, relief="flat")
buttonFrame.pack(fill="x")
butten_packs = {"side":"left", "anchor":"n", "padx":"5"}
button_choice = tk.Button(buttonFrame, text="選擇書籤檔案", command=lambda:File_dialog())
button_choice.pack(butten_packs)
button_save_md = tk.Button(buttonFrame, text="儲存為 md 檔", command=lambda:make_md_list(data_path))
button_save_md.pack(butten_packs)
button_save_txt = tk.Button(buttonFrame, text="儲存為純文字檔",command=lambda:make_txt_list(data_path))
button_save_txt.pack(butten_packs)
butten_exit = tk.Button(buttonFrame, text="關閉程式",command=root.destroy)
butten_exit.pack(butten_packs)

root.mainloop()
