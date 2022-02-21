import gui.templates
import tkinter as tk


class TabBar(gui.templates.Page):
    def _init_elements(self):
        self.__add_button = tk.Button(
            self, text="Add", command=lambda: self._parent.change_tab("add")
        )
        self.__get_button = tk.Button(
            self, text="Get", command=lambda: self._parent.change_tab("get")
        )
        self.__rem_button = tk.Button(
            self, text="Remove", command=lambda: self._parent.change_tab("rem")
        )
        self.__chg_button = tk.Button(
            self, text="Change", command=lambda: self._parent.change_tab("chg")
        )

        self.__add_button.grid(column=0, row=0)
        self.__get_button.grid(column=1, row=0)
        self.__rem_button.grid(column=2, row=0)
        self.__chg_button.grid(column=3, row=0)
