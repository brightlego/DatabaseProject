import gui.page
import gui.tabs
import gui.input
import gui.tabbar
import tkinter as tk

class Gui(gui.page.Page):
    def __init__(self, backend):
        self.__backend = backend
        self.__root = tk.Tk()
        super().__init__(self.__root)

    def _init_elements(self):
        self.__tabbar = gui.tabbar.TabBar(self)
        self.__tab_frame = tk.Frame(self)

        self.__add_tab = gui.tabs.AddTab(self.__tab_frame)
        self.__get_tab = gui.tabs.GetTab(self.__tab_frame)
        self.__rem_tab = gui.tabs.RemoveTab(self.__tab_frame)
        self.__chg_tab = gui.tabs.ChangeTab(self.__tab_frame)

        self.__tab_bar.grid(column=0, row=0)
        self.__tab_frame.grid(column=0, row=1)

        self.__add_tab.grid(column=0, row=0)
        self.__get_tab.grid(column=0, row=0)
        self.__rem_tab.grid(column=0, row=0)
        self.__chg_tab.grid(column=0, row=0)

    def change_tab(self, tab):
        if tab == 'add':
            self.__add_tab.show()
        elif tab == 'get':
            self.__get_tab.show()
        elif tab == 'rem':
            self.__rem_tab.show()
        elif tab == 'chg':
            self.__chg_tab.show()

    def mainloop(self):
        self.__root.mainloop()
