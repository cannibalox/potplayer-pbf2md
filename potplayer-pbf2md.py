import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

# Format Time
def mark_time(line):
    mark_lindex = line.find("=")
    mark_rindex = line.find("*") 
    mark_timeN = line[mark_lindex+1:mark_rindex] # get timestamp
    while len(mark_timeN)<9:
        mark_timeN = "0" + mark_timeN
    #mark_time = "[{0}:{1}:{2}.{3}]".format(mark_timeN[:2], mark_timeN[2:4], mark_timeN[4:6], mark_timeN[6:])
    mark_time = line[mark_lindex+1:mark_rindex-3] # trim timestamp for logseq media-ts
    # format timestamp
    return mark_time


# get bookmartk description
def mark_title(line):
    lindex = line.find("*")  # get index of first * from left
    rindex = line.rfind("*")   # get index of first * from right
    mark_title = line[lindex+1:rindex]   # get text content
    return str(mark_title)

# convert bookmarks to md/text files
def make_list(data_path, save_typ):
    # is there a file to chose ?
    if msgbox("makelist"):
        return None
    folder_name = ""   # use to compare folder names if folder_name != path_split[-2]:
    # pick md/text output format
    if save_typ == "md":   # write markdown
        file_typ = [("Markdown File","*.md")]
        detype = ".md"
        folder_title = "## Folder： "
        file_title = "- "
        def md_write(cun, tim, til):
            return "  - " + cun + ". " + "{{renderer :media-timestamp, " + tim + "}} - "+ til+ "\n"
        endline = "---\n"
    elif save_typ == "txt":   # text write format
        file_typ = [("text file","*.txt")]
        detype = ".text"
        folder_title = "Folder： "
        file_title = "     ---Filename： "
        def md_write(cun, tim, til):
            return "     " + cun + ". "+ tim + " "+ til+ "\n"
        endline = "\n"
    # write file
    with filedialog.asksaveasfile(title="save file", mode="w", defaultextension=detype, filetypes=file_typ) as bml:
        for path in data_path:
            # Get the name of each file in the path
            path_split = path.split("/")
            # Determine whether the folder names are the same. Different: write the folder name. If the same, do not write.
            #if folder_name != path_split[-2]:
            #    bml.write(folder_title + path_split[-2] + "\n")
            #    folder_name = path_split[-2]
            # Open the selected bookmark file
            with open(path, "r", encoding="utf-16LE") as f:
                # Write file name
                bml.write(file_title + path_split[-1][:-4]+ "\n" + "  <video controls=\"true\" style=\"float:left; height:400px\" src=\"file://V:/1_films/" + path_split[-1][:-4] + ".mkv\"></video>\n")
                # Traverse
                count = 0
                for line in f.readlines():
                    if "*" in line:
                        mark_times = mark_time(line)
                        mark_titles = mark_title(line)
                        count += 1  # bookmark number
                        bml.write(md_write(str(count), mark_times, mark_titles))  # Write md file
                bml.write(endline)
            write_progressbar(data_path)

# Show selected files
def show_list(path):
    global list_count
    # Display on file_list Listbox
    file_list.insert("end","[{0}] {1}".format(list_count, path))
    list_count += 1
    return None

#Button function: Search files
def file_select():
    global data_path
    paths = filedialog.askopenfilenames(title="Select bookmark file",
                                          filetype=(("PotPlayer Bookmark File", "*.pbf"),("All Files", "*.*")))
    for path in paths:
        data_path.append(path)
        show_list(path)  # Show selected files
    return None

#Button function: Search all .pbf files in the folder
def folder_select():
    global data_path
    paths = filedialog.askdirectory(title="Select folder")
    for root, dirs, files in os.walk(paths):
        for file_name in files:
            if file_name.endswith(".pbf"):
                path = os.path.join(root, file_name).replace("\\","/")
                data_path.append(path)
                show_list(path)

# Button function: Remove files
def file_delete(deAll = False):
    global data_path
    global list_count
    list_count = 1
    if msgbox("isdelete"):
        # Remove all files
        if deAll:
            del data_path[0:]
            file_list.delete(0, "end")   # Clear List
            return None
        # Remove selected files
        indexs = list(file_list.curselection())
        del data_path[indexs[0]]  # First remove the first one in indexes
            # Iterative removal
        delete_count = 1
        for index in indexs[1:]:   
            del data_path[index-delete_count]   # Each index deletion requires 1
            delete_count += 1
            # Redisplay List
        file_list.delete(0, "end")   # Clear List
        for path in data_path:
            show_list(path)
        return None
    return None

# Create a progress bar
def write_progressbar(data_path):
    global write_times
    file_progressbar["maximum"] = len(data_path)
    write_times += 1
    file_progressbar["value"] = write_times
    root.update()
    return None

# Create dialog box
def msgbox(info, e=None):
    global data_path
    # Dialog-Delete function return False -> Do not execute
    if info == "isdelete":
        if data_path == []:
            messagebox.showerror("Remove files", "No files selected")
            return False
        return messagebox.askokcancel("Remove files", "The selected files will be removed，The actual files will not be deleted\nContinue?")
    #Dialog box -output function return True -> do not execute
    elif info == "makelist":
        if data_path == []:
            messagebox.showerror("save file", "No files selected")
            return True
        return False
    # Dialog exit function
    elif info == "exit":
        if messagebox.askyesno("Close the program", "Are you sure you want to quit ?"):
            root.destroy()
        else:
            return None
    # Dialog exception handling information
    elif info == "exception":
        messagebox.showwarning("Abnormal information", e)

# Create gui
root = tk.Tk()
root.title("Video bookmark integration system")
root.geometry("480x310")
root.resizable(False, False)   # Fixed window size
try:
    root.iconbitmap("logo.ico")
except Exception as i:
    e = str(i) + "\nplease change\"logo.ico\"Files placed in the same folder "
    msgbox("exception", e)
    
data_path = []  #Record selected files
list_count = 1  # Calculate list column number
write_times = 0

# Create ListBox outline
labelFrame = tk.LabelFrame(root, text="Selected files", height=10)
labelFrame.pack(fill="x")
    # Create X,Y scroll
Yaxis_scrollbar = tk.Scrollbar(labelFrame, orient="vertical")
Yaxis_scrollbar.pack(side="right", fill="y")
Xaxis_scrollbar = tk.Scrollbar(labelFrame, orient="horizontal")
Xaxis_scrollbar.pack(side="bottom", fill="x")
    #Create ListBox
file_list = tk.Listbox(labelFrame, height=10,yscrollcommand=Yaxis_scrollbar.set, xscrollcommand=Xaxis_scrollbar.set, 
                        selectmode="extended")
file_list.pack(fill="x", expand="True")
Yaxis_scrollbar.config(command=file_list.yview)
Xaxis_scrollbar.config(command=file_list.xview)

# Create button area outline
button_Frame = tk.LabelFrame(root, relief="flat")
button_Frame.pack(fill="x")
butten_packs = {"side":"left", "padx":"5"}
    # right button
button_r_Frame = tk.LabelFrame(button_Frame, relief="flat")
button_r_Frame.pack(side="right", fill="both", expand=True)
butten_exit = tk.Button(button_r_Frame, width=12, text="Close program", command=lambda:msgbox("exit"))
butten_exit.pack(side="left", fill="y")
    #upper button
button_up_Frame = tk.LabelFrame(button_Frame, relief="flat")
button_up_Frame.pack(padx=10, fill="x")
button_choice = tk.Button(button_up_Frame, text="Select pbf files", width=12, command=lambda:file_select())
button_choice.pack(butten_packs)
button_delete = tk.Button(button_up_Frame, width=12, text="Remove file", command=lambda:file_delete())
button_delete.pack(butten_packs)
button_save_md = tk.Button(button_up_Frame, width=12, text="Save as md file", command=lambda:make_list(data_path, "md"))
button_save_md.pack(butten_packs)
    # Lower button
button_dw_Frame = tk.LabelFrame(button_Frame, relief="flat")
button_dw_Frame.pack(padx=10, fill="x")
button_folder = tk.Button(button_dw_Frame, width=12, text="Search folder", command=lambda:folder_select())
button_folder.pack(butten_packs)
button_delete_all = tk.Button(button_dw_Frame, width=12, text="Remove all files", command=lambda:file_delete(deAll=True))
button_delete_all.pack(butten_packs)
button_save_txt = tk.Button(button_dw_Frame, width=12, text="Save as plain text file", command=lambda:make_list(data_path, "txt"))
button_save_txt.pack(butten_packs)

# Create a progress bar
progressbarFrame = tk.LabelFrame(root, relief="sunken")
progressbarFrame.pack(padx=10, pady=10, fill="x")
file_progressbar = ttk.Progressbar(progressbarFrame, mode="determinate", length=450)
file_progressbar["value"] = 0
file_progressbar.pack()

# style group
    #window style
rootfrmecolor = "#bebebe"
root.configure(bg=rootfrmecolor)
labelFrame.config(bg=rootfrmecolor)
button_Frame.config(bg=rootfrmecolor)
button_r_Frame.config(bg=rootfrmecolor)
button_up_Frame.config(bg=rootfrmecolor)
button_dw_Frame.config(bg=rootfrmecolor)
progressbarFrame.config(bg=rootfrmecolor)
    # button style
buttencolor = "#aaaaaa"
butten_exit.config(bg=buttencolor)
button_choice.config(bg=buttencolor)
button_delete.config(bg=buttencolor)
button_save_md.config(bg=buttencolor)
button_folder.config(bg=buttencolor)
button_delete_all.config(bg=buttencolor)
button_save_txt.config(bg=buttencolor)
    # Listbox style
file_list.config(bg="#D7D6DC")

root.mainloop()
