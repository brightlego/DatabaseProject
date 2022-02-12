import gui.page
import gui.tabs
import gui.input
import tkinter as tk

class Gui(gui.page.Page):
    def __init__(self, backend):
        self.__backend = backend
        self.__root = Tk()
        super().__init__(self.__root)
    
    def _init_elements(self):
        self.__tab_frame = tk.Frame(self)

        self.__add_tab = gui.tabs.AddTab(self.__tab_frame)
        self.__get_tab = gui.tabs.GetTab(self.__tab_frame)
        self.__rem_tab = gui.tabs.RemoveTab(self.__tab_frame)
        self.__chg_tab = gui.tabs.ChangeTab(self.__tab_frame)

        self.__tab_frame.grid(column=0, row=0)

        self.__add_tab.grid(column=0, row=0)
        self.__get_tab.grid(column=0, row=0)
        self.__rem_tab.grid(column=0, row=0)
        self.__chg_tab.grid(column=0, row=0)

    
    def mainloop(self):
        self.__root.mainloop()