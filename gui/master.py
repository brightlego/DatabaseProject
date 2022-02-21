import tkinter as tk

import gui.page
import gui.tabs
import gui.input
import gui.tabbar


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

        self.__input = gui.input.InputField(self)

        self.__tabbar.grid(column=0, row=0)
        self.__tab_frame.grid(column=0, row=1)

        self.__add_tab.grid(column=0, row=0, in_=self.__tab_frame)
        self.__get_tab.grid(column=0, row=0, in_=self.__tab_frame)
        self.__rem_tab.grid(column=0, row=0, in_=self.__tab_frame)
        self.__chg_tab.grid(column=0, row=0, in_=self.__tab_frame)

        self.pack()

    def change_tab(self, tab):
        if tab == "add":
            self.__add_tab.show()  # Show
            self.__get_tab.hide()  #
            self.__rem_tab.hide()  #
            self.__chg_tab.hide()  #
        elif tab == "get":
            self.__add_tab.hide()  #
            self.__get_tab.show()  # Show
            self.__rem_tab.hide()  #
            self.__chg_tab.hide()  #
        elif tab == "rem":
            self.__add_tab.hide()  #
            self.__get_tab.hide()  #
            self.__rem_tab.show()  # Show
            self.__chg_tab.hide()  #
        elif tab == "chg":
            self.__add_tab.hide()  #
            self.__get_tab.hide()  #
            self.__rem_tab.hide()  #
            self.__chg_tab.show()  # Show

    def mainloop(self, *args, **kwargs):
        self.__root.mainloop(*args, **kwargs)
