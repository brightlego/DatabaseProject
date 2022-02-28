import tkinter as tk
from tkinter import ttk

import gui.templates


class OutputBox(gui.templates.HideablePage):
    def _init_elements(self):
        self.__elements = []

    def set_headers(self, headers):
        self.__elements.append(ttk.Separator(self, orient=tk.HORIZONTAL))
        self.__elements[-1].grid(column=0, row=1, columnspan=100, sticky=tk.EW)
        self.__elements.append(ttk.Separator(self, orient=tk.HORIZONTAL))
        self.__elements[-1].grid(column=0, row=3, columnspan=100, sticky=tk.EW)
        self.__elements.append(ttk.Separator(self, orient=tk.VERTICAL))
        self.__elements[-1].grid(column=0, row=0, rowspan=100, sticky=tk.NS)
        column = 1
        for table in headers:
            ttk.Separator(self, orient=tk.VERTICAL).grid(
                column=column + 1, row=0, rowspan=1, sticky=tk.NS
            )
            table_lb = tk.Label(self, text=table)
            table_lb.grid(column=column, columnspan=len(headers[table]), row=0)
            self.__elements.append(table_lb)
            for field in headers[table]:
                ttk.Separator(self, orient=tk.VERTICAL).grid(
                    column=column + 1, row=0, rowspan=100, sticky=tk.NS
                )
                field_lb = tk.Label(self, text=field)
                field_lb.grid(column=column, row=2)
                self.__elements.append(field_lb)
                column += 2

    def set_data(self, data):
        rown = 4
        for row in data:
            column = 1
            for item in row:
                label = tk.Label(self, text=item)
                label.grid(column=column, row=rown, sticky=tk.W)
                self.__elements.append(label)
                column += 2
            rown += 2

    def reset(self):
        for element in self.__elements:
            element.destroy()
        while self.__elements:
            del self.__elements[0]
