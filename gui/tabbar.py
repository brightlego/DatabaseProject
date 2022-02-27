import gui.templates
import tkinter as tk


class TabBar(gui.templates.Page):
    def _init_elements(self):
        self.__variable = tk.StringVar()

        self.__add_button = tk.Radiobutton(
            self,
            text="Add",
            variable=self.__variable,
            value="add",
            indicatoron=False,
            command=lambda: self._parent.change_tab(self.__variable.get()),
            width=20,
            height=2,
        )
        self.__get_button = tk.Radiobutton(
            self,
            text="Get",
            variable=self.__variable,
            value="get",
            indicatoron=False,
            command=lambda: self._parent.change_tab(self.__variable.get()),
            width=20,
            height=2,
        )
        self.__rem_button = tk.Radiobutton(
            self,
            text="Remove",
            variable=self.__variable,
            value="rem",
            indicatoron=False,
            command=lambda: self._parent.change_tab(self.__variable.get()),
            width=20,
            height=2,
        )
        self.__chg_button = tk.Radiobutton(
            self,
            text="Change",
            variable=self.__variable,
            value="chg",
            indicatoron=False,
            command=lambda: self._parent.change_tab(self.__variable.get()),
            width=20,
            height=2,
        )

        self.__add_button.grid(column=0, row=0)
        self.__get_button.grid(column=1, row=0)
        self.__rem_button.grid(column=2, row=0)
        self.__chg_button.grid(column=3, row=0)

        self.bind(
            "<ButtonRelease-1>",
            lambda event: self._parent.change_tab(self.__variable.get()),
        )
