"""Stores the objects for the tabbar to select tabs"""

import tkinter as tk

import gui.templates


class TabBar(gui.templates.Page):
    """The bar to select which tab is open

    Inherits from gui.templates.Page

    Attributes:
        Private:
            __variable (tk.StringVar)
                -- The variable to allow the buttons to be depressed correctly
        Tkinter Widgets:
            __add_button
                -- The button to switch to the add tab
            __get_button
                -- The button to switch to the get tab
            __rem_button
                -- The button to switch to the remove tab
            __chg_button
                -- The button to switch to the change tab
    """

    def _init_elements(self):
        """Initilises the widgets

        Arguments:
            None
        Returns:
            None
        """
        # Create a variable
        self.__variable = tk.StringVar()

        # Create the various buttons
        self.__add_button = tk.Radiobutton(
            self,  # The menubar is the window
            text="Add",
            variable=self.__variable,
            value="add",
            indicatoron=False,  # Makes it button-like not dot-like
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

        # Grid them
        self.__add_button.grid(column=0, row=0)
        self.__get_button.grid(column=1, row=0)
        self.__rem_button.grid(column=2, row=0)
        self.__chg_button.grid(column=3, row=0)
