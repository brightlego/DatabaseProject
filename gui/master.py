import tkinter as tk

import gui.templates
import gui.tabs
import gui.input.input_field
import gui.tabbar
import gui.input.input_xml_cache


class Gui(gui.templates.Page):
    def __init__(self, backend):
        self.__backend = backend
        self.__root = tk.Tk()
        self.__xml_cache = gui.input.input_xml_cache.XMLCache()
        super().__init__(self.__root)

    def _init_elements(self):
        self.__tabbar = gui.tabbar.TabBar(self)
        self.__tabs = gui.tabs.Tabs(self)

        self.__input = gui.input.input_field.InputField(self)

        self.__tabbar.grid(column=0, row=0)
        self.__tabs.grid(column=0, row=1)

        self.change_tab()
        self.pack()

    def get_xml_cache(self):
        return self.__xml_cache

    def change_tab(self, tab=None):
        self.__tabs.change_tab(tab)

    def change_input(self, text):
        print(text)

    def mainloop(self, *args, **kwargs):
        self.__root.mainloop(*args, **kwargs)
