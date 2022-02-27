import tkinter as tk
from tkinter import ttk

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

        self.__input = gui.input.input_field.InputField(
            self, parent_kwargs={"relief": tk.GROOVE}
        )

        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=2, columnspan=100, sticky="ew"
        )

        self.__tabbar.grid(column=0, row=0)
        self.__tabs.grid(column=0, row=1)
        self.__input.grid(column=0, row=3)

        self.change_tab()
        self.pack(expand=True, fill=tk.BOTH)

    def get_xml_cache(self):
        return self.__xml_cache

    def change_tab(self, tab=None):
        self.__tabs.change_tab(tab)

    def change_input(self, template):
        self.__input.set_template(template)

    def gen_new_query(self, type_):
        return self.__backend.gen_new_query(type_)

    def submit_query(self, query):
        print(query.generate_query())
        # self.__backend.handle_query(self.__input.get_query())

    def destroy(self):
        self.__backend.commit()
        super().destroy()

    def undo(self):
        self.__backend.undo()

    def mainloop(self, *args, **kwargs):
        self.__root.mainloop(*args, **kwargs)
