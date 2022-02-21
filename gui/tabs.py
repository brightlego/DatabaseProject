import math
import tkinter as tk
import gui.page as page


def _centre(text, width, filler=" "):
    text = text.rjust(width // 2, filler)
    text = text.ljust(width, filler)
    return text


class _TabButton(tk.Button):
    def __init__(self, master, text, *args, **kwargs):
        self.__text = text
        self.__master = master
        super().__init__(
            master,
            *args,
            text=self.__text,
            command=lambda: self.__master.change_input(text),
            **kwargs,
        )


class __Tab(page.Page):
    _BUTTON_NAMES = []
    _NAME = "Tab"
    _TAB_WIDTH_CHAR = 80
    _BUTTON_WIDTH_CHAR = 10

    def show(self):
        self.grid()

    def hide(self):
        self.grid_remove()

    def _init_elements(self):
        self._buttons = {}
        self._label = tk.Label(self, text=f"{self._NAME}:")
        self._label.grid(column=0, row=0)
        row = 1
        column = 0
        for button in self._BUTTON_NAMES:
            columnspan = math.ceil(len(button) / self._BUTTON_WIDTH_CHAR)
            rowspan = math.ceil(len(button) / self._TAB_WIDTH_CHAR)
            if rowspan > 1:
                columnspan = self._TAB_WIDTH_CHAR // self._BUTTON_WIDTH_CHAR
            if (
                rowspan > 1
                or column + columnspan > self._TAB_WIDTH_CHAR / self._BUTTON_WIDTH_CHAR
            ):
                column = 0

            if rowspan == 1:
                button = _centre(button, self._BUTTON_WIDTH_CHAR)
            else:
                button = [
                    _centre(button[i : i + self._TAB_WIDTH_CHAR], self._TAB_WIDTH_CHAR)
                    for i in range(0, len(button), self._TAB_WIDTH_CHAR)
                ]
                button = "\n".join(button)
            self._buttons[button] = _TabButton(self, button)
            if column == 0:
                self._buttons[button].grid(
                    row=row + 1,
                    column=column + 1,
                    columnspan=columnspan,
                    rowspan=rowspan,
                )
                row += rowspan
                column += columnspan
            else:
                self._buttons[button].grid(
                    row=row, column=column + 1, columnspan=columnspan, rowspan=rowspan
                )
                column += columnspan


class AddTab(__Tab):
    _BUTTON_NAMES = ["Test1", "Test 11"]


class GetTab(__Tab):
    _BUTTON_NAMES = ["Test2"]


class RemoveTab(__Tab):
    _BUTTON_NAMES = ["Test3"]


class ChangeTab(__Tab):
    _BUTTON_NAMES = ["Test4"]
