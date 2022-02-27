import tkinter as tk


class Page(tk.Frame):
    def __init__(self, parent, *args, parent_kwargs=None, **kwargs):
        self._parent = parent
        if parent_kwargs is None:
            parent_kwargs = {}
        super().__init__(parent, **parent_kwargs)
        self._init_elements(*args, **kwargs)

    def _init_elements(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return self.__getattribute__(name)


class HollowPage(Page):
    def __getattr__(self, name):
        return self._parent.__getattr__(name)


class HideablePage(Page):
    def show(self):
        self.grid()

    def hide(self):
        self.grid_remove()
