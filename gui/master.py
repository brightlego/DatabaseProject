import tkinter as tk
import tkinter.messagebox as tkmessagebox
from tkinter import ttk

import gui.templates
import gui.tabs
import gui.input.input_field
import gui.tabbar
import gui.input.input_xml_cache
import gui.undo
import gui.output


class Gui(gui.templates.Page):
    def __init__(self, backend):
        self.__backend = backend
        self.__root = GuiRoot(self)
        self.__xml_cache = gui.input.input_xml_cache.XMLCache()
        super().__init__(self.__root)

    def _init_elements(self):
        self.__tabbar = gui.tabbar.TabBar(self)
        self.__tabs = gui.tabs.Tabs(self)

        self.__input = gui.input.input_field.InputField(
            self, parent_kwargs={"relief": tk.GROOVE}
        )
        self.__input_is_empty = True

        self.__output = gui.output.OutputBox(self)

        self.__undo_buton = gui.undo.UndoButton(self)

        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=2, columnspan=100, sticky=tk.EW
        )
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=4, columnspan=100, sticky=tk.EW
        )
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=6, columnspan=100, sticky=tk.EW
        )

        self.__tabbar.grid(column=0, row=0, sticky=tk.W)
        self.__tabs.grid(column=0, row=1, pady=5, sticky=tk.W)
        self.__input.grid(column=0, row=3)
        self.__input.grid_remove()
        self.__undo_buton.grid(column=0, row=5, sticky=tk.W)
        self.__output.grid(column=0, row=7)

        self.change_tab()
        self.config(relief="ridge")
        self.pack(expand=True, fill=tk.BOTH)

    def get_xml_cache(self):
        return self.__xml_cache

    def change_tab(self, tab=None):
        self.__tabs.change_tab(tab)

    def change_input(self, template):
        if self.__input_is_empty:
            self.__input.grid()
        self.__input_is_empty = False
        self.__input.set_template(template)

    def gen_new_query(self, type_):
        return self.__backend.gen_new_query(type_)

    def submit_query(self, query):
        fields = query.get_fields()
        data = self.__backend.handle_query(query)
        if fields:
            self.__output.reset()
            self.__output.set_headers(fields)
            self.__output.set_data(data)

    def commit(self):
        self.__backend.commit()

    def rollback(self):
        self.__backend.rollback()

    def undo(self):
        self.__backend.undo()

    def mainloop(self, *args, **kwargs):
        self.__root.mainloop(*args, **kwargs)


class GuiRoot(tk.Tk):
    def __init__(self, gui):
        self.__gui = gui
        super().__init__()

    def destroy(self):
        answer = tkmessagebox.askyesnocancel(
            title="Exiting", message="Do you want to save changes to the database?"
        )
        if answer is None:
            return
        elif answer:
            self.__gui.commit()
            super().destroy()
        else:
            self.__gui.rollback()
            super().destroy()
