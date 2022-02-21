import math
import tkinter as tk
import gui.templates


def _centre(text, width, filler=" "):
    text = text.rjust(width // 2, filler)
    text = text.ljust(width, filler)
    return text


class Tabs(gui.templates.Page):
    def _init_elements(self):
        self.__add_tab = gui.tabs.AddTab(self)
        self.__get_tab = gui.tabs.GetTab(self)
        self.__rem_tab = gui.tabs.RemoveTab(self)
        self.__chg_tab = gui.tabs.ChangeTab(self)

        self.__add_tab.grid(column=0, row=0, sticky=tk.W)
        self.__get_tab.grid(column=0, row=0, sticky=tk.W)
        self.__rem_tab.grid(column=0, row=0, sticky=tk.W)
        self.__chg_tab.grid(column=0, row=0, sticky=tk.W)

    def change_tab(self, tab=None):
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
        elif tab is None:
            self.__add_tab.hide()  #
            self.__get_tab.hide()  #
            self.__rem_tab.hide()  #
            self.__chg_tab.hide()  #

    def change_input(self, text):
        self._parent.change_input(text)


class _TabButton(tk.Button):
    def __init__(self, parent, text, command, *args, **kwargs):
        self.__text = text
        self.__parent = parent
        super().__init__(
            parent,
            *args,
            text=self.__text,
            command=lambda: self.__parent.change_input(command),
            **kwargs,
        )


class __Tab(gui.templates.HideablePage):
    _BUTTON_NAMES = []
    _NAME = "Tab"
    _TAB_WIDTH_CHAR = 80
    _BUTTON_WIDTH_CHAR = 10

    def change_input(self, text):
        self._parent.change_input(text)

    def __get_column_rowspan(self, button, column, row):
        columnspan = math.ceil(len(button) / self._BUTTON_WIDTH_CHAR)
        rowspan = math.ceil(len(button) / self._TAB_WIDTH_CHAR)
        if rowspan > 1:
            columnspan = self._TAB_WIDTH_CHAR // self._BUTTON_WIDTH_CHAR
        if (
            rowspan > 1
            or column + columnspan > self._TAB_WIDTH_CHAR / self._BUTTON_WIDTH_CHAR
        ):
            column = 0

        return columnspan, rowspan, column, row

    def __format_button_label(self, button, columnspan):
        if len(button) > self._TAB_WIDTH_CHAR:
            button = [
                button[i : i + self._TAB_WIDTH_CHAR]
                for i in range(0, len(button), self._TAB_WIDTH_CHAR)
            ]
            button = [_centre(line, self._TAB_WIDTH_CHAR) for line in button]
            button = "\n".join(button)
        else:
            button = _centre(button, self._BUTTON_WIDTH_CHAR * columnspan)
        return button

    def _init_elements(self):
        self._buttons = {}
        self._label = tk.Label(self, text=f"{self._NAME}:")
        self._label.grid(column=0, row=0)
        row = 1
        column = 0
        for button in self._BUTTON_NAMES:
            columnspan, rowspan, column, row = self.__get_column_rowspan(
                button, column, row
            )

            formatted_button = self.__format_button_label(button, columnspan)

            self._buttons[button] = _TabButton(self, formatted_button, button)

            if column == 0:
                self._buttons[button].grid(
                    row=row + 1,
                    column=column + 1,
                    columnspan=columnspan,
                    rowspan=rowspan,
                    sticky=tk.W,
                )
                row += rowspan
                column += columnspan
            else:
                self._buttons[button].grid(
                    row=row,
                    column=column + 1,
                    columnspan=columnspan,
                    rowspan=rowspan,
                    sticky=tk.W,
                )
                column += columnspan


class AddTab(__Tab):
    _NAME = "Add"
    _BUTTON_NAMES = ["Test1", "Test 11"]


class GetTab(__Tab):
    _NAME = "Get"
    _BUTTON_NAMES = ["Test2"]


class RemoveTab(__Tab):
    _NAME = "Remove"
    _BUTTON_NAMES = ["Test3"]


class ChangeTab(__Tab):
    _NAME = "Change"
    _BUTTON_NAMES = ["Test4"]
