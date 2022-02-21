import tkinter as tk


class Page(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self._parent = parent
        super().__init__(parent)
        self._init_elements(*args, **kwargs)

    def _init_elements(self, *args, **kwargs):
        pass


class HideablePage(Page):
    def show(self):
        self.grid()

    def hide(self):
        self.grid_remove()
