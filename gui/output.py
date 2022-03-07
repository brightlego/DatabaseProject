"""The file that holds the object to do with the output box"""

import tkinter as tk
from tkinter import ttk

import gui.templates


class OutputBox(gui.templates.HideablePage):
    """The box which holds the output

    Attributes:
        Tkinter widgets:
            __elements (list[tkinter.Seperator|tkinter.Label])
                -- The elements in the output box

    Methods:
        Overridden:
            _init_elements() -> None
        Public:
            set_headers(headers: dict[str:list[str]]) -> None
                -- Sets the header of the output table
            set_data(data: list[][]) -> None
                -- Sets the data in the table to that specified by data
    """

    def _init_elements(self):
        """Initiates the elements

        Arguments:
            None

        Returns:
            None
        """
        self.__elements = []

    def set_headers(self, headers):
        """Sets the header of the output table

        Arguments:
            headers (dict[str:list[str]])
                -- The headers to set to that specified in headers

        Returns:
            None
        """

        # Sets the first column to 1
        column = 1

        # For each table in the headers
        for table in headers:

            # If there are no fields in that table, ignore it
            if len(headers[table]) == 0:
                continue

            # Add a vertical seperator between this major header and the next
            self.__elements.append(ttk.Separator(self, orient=tk.VERTICAL))
            self.__elements[-1].grid(
                column=column + len(headers[table]) * 2 - 1,
                row=0,
                rowspan=100,
                sticky=tk.NS,
            )

            # Create the label for the major header
            table_lb = tk.Label(self, text=table)
            table_lb.grid(column=column, columnspan=len(headers[table]), row=0)
            self.__elements.append(table_lb)

            # For each field in the table
            for field in headers[table]:

                # Create a seperator between the minor headers
                self.__elements.append(ttk.Separator(self, orient=tk.VERTICAL))
                self.__elements[-1].grid(
                    column=column + 1, row=1, rowspan=100, sticky=tk.NS
                )

                # Create the lable for the minor header
                field_lb = tk.Label(self, text=field)
                field_lb.grid(column=column, row=2)
                self.__elements.append(field_lb)

                # Increment the column by 2 (for the seperator and the label)
                column += 2

            # Increment the column by 2 again for the other seperator
            column += 2

        # Create the seperators betweent he minor headers and the major headers
        self.__elements.append(ttk.Separator(self, orient=tk.HORIZONTAL))
        self.__elements[-1].grid(column=0, row=1, columnspan=100, sticky=tk.EW)
        self.__elements.append(ttk.Separator(self, orient=tk.HORIZONTAL))
        self.__elements[-1].grid(column=0, row=3, columnspan=100, sticky=tk.EW)

        # Create a seperator at the begining because relief refuses to work
        self.__elements.append(ttk.Separator(self, orient=tk.VERTICAL))
        self.__elements[-1].grid(column=0, row=0, rowspan=100, sticky=tk.NS)

    def set_data(self, data):
        """Sets the data to that spefified in data

        Arguments:
            data (list[][])
                -- The data to set

        Returns:
            None
        """

        # The Row number
        rown = 4

        # For each row in the data
        for row in data:

            # Set the column to 1
            column = 1

            # For each item in the row
            for item in row:

                # Create a label for that item
                label = tk.Label(self, text=item)
                label.grid(column=column, row=rown, sticky=tk.W)
                self.__elements.append(label)

                # Increase the row by 2 (seperator and label)
                column += 2
            rown += 1

    def reset(self):
        """Reset the output box

        Arguments:
            None

        Returns:
            None
        """

        # Destroy every element
        for element in self.__elements:
            element.destroy()

        # Make sure the elements are really gone
        while self.__elements:
            del self.__elements[0]
