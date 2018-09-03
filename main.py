# This Python file uses the following encoding: utf-8
import mko
import tkinter as tk
from tkinter import filedialog
import mko_unit_frame
import os
import configparser


def delete_unit():
    num = int(unit_var.get())
    mko_frame.delete_unit_by_num(num)
    pass


def load_cfg():
    config = configparser.ConfigParser()
    home_dir = os.getcwd()
    try:
        os.mkdir(home_dir + "\\Config")
    except OSError:
        pass
    root.filename = filedialog.askopenfilename(initialdir=home_dir + "\\Config",
                                               title="Select file",
                                               filetypes=(("cfg files", "*.cfg"), ("all files", "*.*"))
                                               )
    config.read(root.filename)
    mko_frame.load_cfg(config)
    pass


def save_cfg():
    home_dir = os.getcwd()

    config = configparser.ConfigParser()
    config = mko_frame.get_cfg(config)

    try:
        os.mkdir(home_dir + "\\Config")
    except OSError:
        pass
    root.filename = filedialog.asksaveasfilename(initialdir=home_dir + "\\Config",
                                                 title="Select file",
                                                 filetypes=(("cfg files", "*.cfg"), ("all files", "*.*"))
                                                 )
    try:
        with open(root.filename, 'w') as configfile:
            config.write(configfile)
    except FileNotFoundError:
        pass
    pass


# Main window
root = tk.Tk()
root.title("MKO Test")
root.geometry('900x700')
root.resizable(False, False)

# ta1
ta1 = mko.TA1()

# mko frame
mko_frame = mko_unit_frame.MkoFrame(root)
mko_frame.place(x=5, y=0, width=670, relheight=1, height=0)

# управление элементами
add_unit_button = tk.Button(root, text="Добавить элемент", command=mko_frame.add_unit)
add_unit_button.place(x=700, y=5, width=150, height=25)

unit_var = tk.StringVar(root)
unit_var.set("0")
unit_entry = tk.Entry(root, width=5, bd=2, textvariable=unit_var, justify="right")
unit_entry.place(x=855, y=30)

cfg_save_button = tk.Button(root, text="Удалить элемент", command=delete_unit)
cfg_save_button.place(x=700, y=30, width=150, height=25)

# сохранение-загрузка конфигурации
cfg_load_button = tk.Button(root, text="Загрузить конф.", command=load_cfg)
cfg_load_button.place(x=700, y=60, width=150, height=25)

cfg_save_button = tk.Button(root, text="Сохранить конф.", command=save_cfg)
cfg_save_button.place(x=700, y=90, width=150, height=25)
#
# Main
root.mainloop()
