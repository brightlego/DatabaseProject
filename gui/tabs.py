import tkinter as tk
import gui.page as page

class __Tab(page.Page):
    def show(self):
        self.lift()

class AddTab(__Tab):
    pass

class GetTab(__Tab):
    pass

class RemoveTab(__Tab):
    pass

class ChangeTab(__Tab):
    pass