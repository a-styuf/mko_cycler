import tkinter as tk
import tk_table
import Pmw
from mko import *
import configparser
import random


class MkoUnit(tk.Frame):
    def __init__(self, parent, **kw):
        self.num = 0
        self.name = "..."
        for key in sorted(kw):
            if key == "mko":
                self.mko = kw.pop(key)
            elif key == "num":
                self.num = kw.pop(key)
            elif key == "name":
                self.name = kw.pop(key)
            else:
                pass
        tk.Frame.__init__(self, parent, kw)

        # инициаллизация МКО #
        self.ta1_mko = TA1()
        self.ta1_mko.init()
        # конфигурация
        self.cfg_dict = {"addr": "22",
                         "subaddr": "1",
                         "leng": "32",
                         "data": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
                         "name": ""
                         }
        self.state = 0
        self.action_state = 0
        self.bus_state = 0
        self.addr = 0
        self.subaddr = 0
        self.leng = 0
        self.data = [0, 0]
        #
        self.gui_set()
        self.load_cfg()
        pass

    def gui_set(self):
        # frame label
        self.num_var = tk.StringVar(self)
        self.num_var.set(self.num)
        self.num_entry = tk.Label(self, width=3, bd=2, textvariable=self.num_var)
        self.num_entry.place(x=0, y=5)

        self.label_var = tk.StringVar(self)
        self.label_var.set(self.name)
        self.label_entry = tk.Entry(
            self, width=30, bd=2, textvariable=self.label_var, justify="left", relief="flat", bg="gray98"
            )
        self.label_entry.place(x=30, y=5)

        # ввод параметров отправки
        input_x = 0
        input_y = 35
        self.mko_addr_var = tk.StringVar(self)
        self.mko_addr_var.set("19")

        tk.Label(self, width=10, bd=2, text="Адрес:", anchor="w").place(x=input_x + 5, y=input_y + 0)
        self.mko_addr_entry = tk.Entry(self, width=3, bd=2, textvariable=self.mko_addr_var, justify="right")
        self.mko_addr_entry.place(x=input_x + 50, y=input_y + 0)

        self.mko_subaddr_var = tk.StringVar(self)
        self.mko_subaddr_var.set("30")

        tk.Label(self, width=10, bd=2, text="Субадр:", anchor="w").place(x=input_x + 75, y=input_y + 0)
        self.mko_subaddr_entry = tk.Entry(self, width=3, bd=2, textvariable=self.mko_subaddr_var, justify="right")
        self.mko_subaddr_entry.place(x=input_x + 125, y=input_y + 0)

        self.mko_len_var = tk.StringVar(self)
        self.mko_len_var.set("32")

        tk.Label(self, width=10, bd=2, text="Длина:", anchor="w").place(x=input_x + 150, y=input_y + 0)
        self.mko_len_entry = tk.Entry(self, width=3, bd=2, textvariable=self.mko_len_var, justify="right")
        self.mko_len_entry.place(x=input_x + 200, y=input_y + 0)

        # вывод данных об транзакции
        output_x = 0
        output_y = 95

        self.mko_com_word = tk.StringVar(self)
        self.mko_com_word.set(" ")
        tk.Label(self, width=10, bd=2, text="КC:", anchor="w").place(x=output_x + 5, y=output_y + 0)
        self.mko_com_entry = tk.Entry(self, width=7, bd=2, textvariable=self.mko_com_word)
        self.mko_com_entry.place(x=output_x + 30, y=output_y + 0)

        self.mko_answ_word = tk.StringVar(self)
        self.mko_answ_word.set(" ")
        tk.Label(self, width=10, bd=2, text="ОC:", anchor="w").place(x=output_x + 80, y=output_y + 0)
        self.mko_answ_entry = tk.Entry(self, width=7, bd=2, textvariable=self.mko_answ_word)
        self.mko_answ_entry.place(x=output_x + 105, y=output_y + 0)

        self.status_led = tk.Label(self, width=5, bd=2, text="МКО", anchor="w", bg="gray80")
        self.status_led.place(x=output_x + 160, y=output_y + 0)

        self.bus_status_led = tk.Label(self, width=5, bd=2, text="Линия", anchor="w", bg="gray80")
        self.bus_status_led .place(x=output_x + 210, y=output_y + 0)

        #запуск действия
        act_x = 0
        act_y = 65

        self.action_checkbutton = tk.Checkbutton(self, text="Чтение", command=self.action_choose)
        self.action_checkbutton.place(x=act_x + 5, y=act_y + 1)

        self.read_button = tk.Button(self, text="Пуск", command=self.action)
        self.read_button.place(x=act_x + 100, y=act_y + 0, width=150, height=25)

        # тыблицы для вывод данных
        self.mko_table = tk_table.data_table(self, rows=5, text=random_smile())
        self.mko_table.place(x=270, y=25)
        pass



    def load_cfg(self, cfg_dict=None):
        if cfg_dict:
            self.cfg_dict = cfg_dict
        self.name = self.cfg_dict["name"]
        self.label_var.set(self.name)
        self.addr = self.cfg_dict["addr"]
        self.mko_addr_var.set(self.addr)
        self.subaddr = self.cfg_dict["subaddr"]
        self.mko_subaddr_var.set(self.subaddr)
        self.leng = self.cfg_dict["leng"]
        self.mko_len_var.set(self.leng)
        self.data = [int(var, 16) for var in self.cfg_dict["data"].split(" ")]
        self.mko_table.InsertData(self.data)
        pass

    def get_cfg(self):
        self.name = self.label_var.get()
        self.cfg_dict["name"] = self.name
        self.addr = self.mko_addr_var.get()
        self.cfg_dict["addr"] = self.addr
        self.subaddr = self.mko_subaddr_var.get()
        self.cfg_dict["subaddr"] = self.subaddr
        self.leng = self.mko_len_var.get()
        self.cfg_dict["leng"] = self.leng
        self.data = self.mko_table.GetData()
        self.cfg_dict["data"] = " ".join(["%04X" % var for var in self.data])
        return self.cfg_dict

    def write(self):
        self.connect()
        self.ta1_mko.SendToRT\
            (int(self.mko_addr_var.get()), int(self.mko_subaddr_var.get()),
             self.mko_table.GetData(), int(self.mko_len_var.get()))
        self.mko_answ_word.set("0x{:04X}".format(self.ta1_mko.answer_word))
        self.mko_com_word.set("0x{:04X}".format(self.ta1_mko.command_word))
        self.state_check()
        self.ta1_mko.disconnect()
        pass

    def read(self):
        self.connect()
        self.mko_table.InsertData(self.ta1_mko.ReadFromRT\
            (int(self.mko_addr_var.get()), int(self.mko_subaddr_var.get()), int(self.mko_len_var.get())))
        self.mko_answ_word.set("0x{:04X}".format(self.ta1_mko.answer_word))
        self.mko_com_word.set("0x{:04X}".format(self.ta1_mko.command_word))
        self.ta1_mko.disconnect()
        self.state_check()
        pass

    def action(self):
        if self.action_state == 0:  # read
            self.read()
        else:
            self.write()
        pass

    def state_check(self):
        if self.ta1_mko.state == 0:
            self.status_led["bg"] = "PaleGreen3"
        elif self.ta1_mko.state == 1:
            self.status_led["bg"] = "coral2"
        if self.ta1_mko.bus_state == 1:
            self.bus_status_led["bg"] = "PaleGreen3"
        elif self.ta1_mko.bus_state == 0:
            self.bus_status_led["bg"] = "coral2"
        pass

    def connect(self):
        self.state = self.ta1_mko.init()
        return self.state

    def action_choose(self):
        if self.action_checkbutton["text"] == "Чтение":
            self.action_checkbutton["text"] = "Запись"
            self.action_state = 1
        else:
           self.action_checkbutton["text"] = "Чтение"
           self.action_state = 0
        pass


class MkoFrame(tk.Canvas):
    def __init__(self, parent, **kw):

        self.mko_unit_list = []

        tk.Canvas.__init__(self, parent, kw)
        self.frame = tk.Frame(self)
        self.y_scrollbar = tk.Scrollbar(self, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=self.y_scrollbar.set)
        #
        # объявление дополнительных параметров
        self.frame_window = self.create_window(0, 0, anchor='nw', window=self.frame)
        self._frame_position = [0, 0, 0, 0]
        self.redraw()

    def gui_set(self):

        pass

    def add_unit(self):
        self.mko_unit_list.append(
            MkoUnit(self.frame, num=len(self.mko_unit_list), width=650, height=135, bd=2, relief="groove")
            )
        self.mko_unit_list[-1].grid()  # place(x=0, y=150*(len(self.mko_unit_list)-1))
        pass

    def delete_unit_by_num(self, n):
        try:
            self.mko_unit_list.pop(n).destroy()
            for i in range(len(self.mko_unit_list)):
                self.mko_unit_list[i].num = i
        except IndexError:
            pass
        pass

    def delete_all_units(self):
        for unit in self.mko_unit_list:
            unit.destroy()
        self.mko_unit_list = []
        pass

    def redraw(self):
        #
        self.y_scrollbar.pack(side="right", fill="y")
        self.y_scrollbar.configure(command=self.yview)
        self.configure(yscrollcommand=self.y_scrollbar.set)
        self.frame.bind('<Configure>', lambda event: self.configure(scrollregion=self.bbox('all')))
        pass

    def place_(self, cnf={}, **kw):
        self.place(cnf={}, **kw)
        self.redraw()

    def get_cfg(self, config):
        for i in range(len(self.mko_unit_list)):
            cfg_dict = self.mko_unit_list[i].get_cfg()
            print(cfg_dict)
            config[str(i)] = cfg_dict
        return config

    def load_cfg(self, config):
        units_cfg = config.sections()
        print(units_cfg)
        self.delete_all_units()
        for i in range(len(units_cfg)):
            self.add_unit()
            self.mko_unit_list[-1].load_cfg(config[units_cfg[i]])
        return config


def random_smile():
    smiles = [
        "(＃＞＜)", "(✿｡✿)", "⊙﹏⊙", "(￣0￣)", "(¬‿¬)",
        "(◑‿◐)", "(◕‿◕)", "(✪㉨✪)", "(⊙_⊙)", "(＾▽＾)"
    ]
    return random.choice(smiles)
