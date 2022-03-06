import math
import tkinter as tk

import gui.templates


def _centre(text, width, filler=" "):
    """Centres text

    Arguments:
        text (str)
            -- Text to centre
        width (int)
            -- The width of the text

    Keyword Arguments:
        filler (str) default " "
            -- The filler character

    Returns
        text (str)
            -- The centred text
    """
    count_to_add = width - len(text)
    text = text.rjust(math.ceil((len(text) + width) / 2), filler)
    text = text.ljust(width, filler)
    return text


class Tabs(gui.templates.Page):
    """The holder for the various tabs

    Inherits from gui.templates.Page.

    Attributes:
        Private:
            __variable (tkinter.StringVar)
                -- The variable used in the buttons

        Tkinter Widgets:
            __add_tab (gui.tabs.AddTab)
                -- The tab with the buttons for adding data
            __get_tab (gui.tabs.GetTab)
                -- The tab with the buttons for getting data
            __rem_tab (gui.tabs.RemoveTab)
                -- The tab with the buttons for removing data
            __chg_tab (gui.tabs.ChangeTab)
                -- The tab with the buttons for changing data

    Methods:
        Overridden:
            _init_elements() -> None

        Public:
            change_tab(tab:str=None) -> None
                -- Changes the tab to the tab specified by tab
            change_input(template: xml.etree.ElementTree) -> None
                -- Relays the text from a tab to change_input in gui.master.Gui
            get_tab_var() -> tk.StringVar
                -- Returns the variable which holds the button which has been
                   pressed
            get_xml_cache() -> xml.etree.ElementTree
                -- Relays the XML cahce from gui.maser.Gui to a tab
    """

    def _init_elements(self):
        """Initiates the tkinter elements

        Arguments:
            None

        Returns:
            None
        """
        # The variable used in the RadioButtons within the tabs
        self.__variable = tk.StringVar()

        # The tabs
        self.__add_tab = gui.tabs.AddTab(self)
        self.__get_tab = gui.tabs.GetTab(self)
        self.__rem_tab = gui.tabs.RemoveTab(self)
        self.__chg_tab = gui.tabs.ChangeTab(self)

        # Grid the tabs over each other and sticky westwards
        self.__add_tab.grid(column=0, row=0, sticky=tk.W)
        self.__get_tab.grid(column=0, row=0, sticky=tk.W)
        self.__rem_tab.grid(column=0, row=0, sticky=tk.W)
        self.__chg_tab.grid(column=0, row=0, sticky=tk.W)

    def change_tab(self, tab=None):
        """Changes the tab to that specified by tab

        Arguments:
            None

        Keyword Arguments:
            tab (str) default None
                -- The tab to change to

        Returns:
            None
        """
        # Make the tab case-insensitive
        if tab is not None:
            tab = tab.lower()

        # Hide all the tabs
        self.__add_tab.hide()
        self.__get_tab.hide()
        self.__rem_tab.hide()
        self.__chg_tab.hide()

        # Show only the ones that are specified by `tab`
        if tab == "add":
            self.__add_tab.show()
        elif tab == "get":
            self.__get_tab.show()
        elif tab == "rem":
            self.__rem_tab.show()
        elif tab == "chg":
            self.__chg_tab.show()

        # If tab is None, show none of them.

    def change_input(self, template):
        """Relays what to change the input field to as specified in `text`.

        Relays from a child of gui.tabs.Tab to gui.master.Gui

        Arguments:
            template (xml.etree.ElementTree)
                -- The template of the new part of InputField

        Returns:
            None
        """
        self._parent.change_input(template)

    def get_tab_var(self):
        """Accessor method for __variable"""
        return self.__variable

    def get_xml_cache(self):
        """Relays the XML Cache.

        Relays from gui.master.Gui to a child of gui.tabs.__tabs

        Arguments:
            None

        Returns:
            xml_cache (xml.etree.ElementTree)
                -- The cache of xml data for input field
        """
        return self._parent.get_xml_cache()


class TabButton(tk.Radiobutton):
    """A RadioButton used to specify which input field and used within a tab.

    Inherits from tkinter.Radiobutton.

    Attributes:
        Private:
            __text (str)
                -- The text of the button
            __parent (gui.templates.Page)
                -- The parent page of the button
            __variable (tkinter.StringVar)
                -- The variable used in the button

    Methods:
        Overwridden:
            __init__(parent: gui.templates.Page,
                     text: str,
                     command: xml.etree.ElementTree,
                     width: int,
                     height: int,
                     *args,
                     **kwargs
                     ) -> None
    """

    def __init__(self, parent, text, command, width, height, *args, **kwargs):
        """The Constructor for TabButton

        *args and **kwargs are passed to tkinter.RadioButton constructor

        Arguments:
            parent (gui.templates.Page)
                -- The parent to this element
            text (str)
                -- The text on the button
            command (xml.etree.ElementTree)
                -- The input field template to change to when the button is
                   pressed
            width (int)
                -- The width of the button in characters
            height (int)
                -- The height of the button in characters
        """
        self.__text = text
        self.__parent = parent

        # Get the variable used in the button from the parent
        # This is so only one button can be depressed at a time
        self.__variable = self.get_variable()
        super().__init__(
            parent,
            *args,
            text=self.__text,
            variable=self.__variable,
            value=self.__text,
            command=lambda: self.__parent.change_input(command),
            width=width,
            height=height + 1,
            indicatoron=False,
            **kwargs,
        )

        # Make sure that no button is selected at first
        self.deselect()


class Tab(gui.templates.HideablePage):
    """A tab which hold the buttons to chagne the input.

    Inherits from gui.templates.HideablePage

    Attributes:
        Static:
            _TAB_WIDTH_CHAR (int)
                -- The width of the tab in characters
            _BUTTON_WIDTH_CHAR (int)
                -- The minimum width of the button in characters
        Protected:
            _variable (tkinter.StringVar)
                -- The variable for the buttons

        Tkinter Widgets:
            _buttons (dict[str : gui.tabs.TabButton])
                -- The buttons in the tab

    Methods:
        Overwridden:
            _init_elements() -> None

        Public:
            change_input(tempalte: xml.etree.ElementTree) -> None
                -- Relay for template from TabButton to Tabs
            get_variable() -> tkinter.StringVar
                -- Relay for _variable from TabButton to Tabs
        Protected:
            _get_button_names() -> list[str]
                -- Gets the names of the buttons
            _get_xml_cache() -> xml.etree.ElementTree
                -- Gets the xml cache for the buttons
        Private:
            __get_column_rowspan(button: str, column: int, row: int)
                -- Gets the columnspan and the rowspan for a certian button
            __format_button_label(button: str, columnspan: int)
                -- Formats the button's label
    """

    _TAB_WIDTH_CHAR = 80
    _BUTTON_WIDTH_CHAR = 10

    def _init_elements(self):
        """Initilises the buttons int he tab

        Arguments:
            None

        Returns:
            None
        """

        # Create a variable for the tabs
        self._variable = tk.StringVar()

        # The buttons
        self._buttons = {}

        # Start at row 1 and column 0
        row = 1
        column = 0

        # Iterate through the button names
        for button in self._get_button_names():

            # Get the columnspan and the row span and ajust column and
            # row accordingly
            columnspan, rowspan, column, row = self.__get_column_rowspan(
                button, column, row
            )

            # Format the button
            formatted_button = self.__format_button_label(button, columnspan)

            # Create that button
            self._buttons[button] = TabButton(
                self,
                formatted_button,
                self._get_xml_cache(button),
                columnspan * self._BUTTON_WIDTH_CHAR,
                rowspan,
            )

            # Grid the button
            if column == 0:
                self._buttons[button].grid(
                    row=row + 1,  # Move onto the next row
                    column=column,
                    columnspan=columnspan,
                    rowspan=rowspan,
                    sticky=tk.W,
                )
                row += rowspan  # Add onto rowspan
                column += columnspan
            else:
                self._buttons[button].grid(
                    row=row,
                    column=column,
                    columnspan=columnspan,
                    rowspan=rowspan,
                    sticky=tk.W,
                )
                column += columnspan

    def change_input(self, template):
        """Relay for template from TabButton to Tabs"""
        self._parent.change_input(template)

    def __get_column_rowspan(self, button, column, row):
        """Gets the columnspan and the rowspan for a certian button

        Arguments:
            button (str)
                -- The label for the button
            column (int)
                -- The current column
            row (int)
                -- The current row
        Returns:
            columnspan (int)
                -- The columnspan
            rowspan (int)
                -- The rowspan
            column (int)
                -- The new column
            row (int)
                -- The new row
        """

        # Get how many columns and rows the button passes and round up
        columnspan = math.ceil(len(button) / self._BUTTON_WIDTH_CHAR)
        rowspan = math.ceil(len(button) / self._TAB_WIDTH_CHAR)

        # If the button spans more than 1 row
        if rowspan > 1:
            # Set the columnspan to the width of the tab in the min widths of
            # the button.
            columnspan = self._TAB_WIDTH_CHAR // self._BUTTON_WIDTH_CHAR

        # If the button takes up more than 1 row or wraps onto the next row
        if (
            rowspan > 1
            or column + columnspan > self._TAB_WIDTH_CHAR / self._BUTTON_WIDTH_CHAR
        ):
            # Set the column to 0
            column = 0

        return columnspan, rowspan, column, row

    def __format_button_label(self, button, columnspan):
        """Formats the button's label

        Arguments:
            button (str)
                -- The label of the button
            columnspan (int)
                -- How many colums the button goes across

        Returns:
            button (str)
                -- The formatted button
        """

        # If the button label takes up more than 1 lines
        if len(button) > self._TAB_WIDTH_CHAR:
            # Split it up into chunks of equal width to the tab
            button = [
                button[i : i + self._TAB_WIDTH_CHAR]
                for i in range(0, len(button), self._TAB_WIDTH_CHAR)
            ]
            # Centre these chunks
            button = [_centre(line, self._TAB_WIDTH_CHAR) for line in button]

            # Join these chunks with newlines
            button = "\n".join(button)
        else:
            # Otherwise, centre the button
            button = _centre(button, self._BUTTON_WIDTH_CHAR * columnspan)
        return button

    def get_variable(self):
        """Relay for _variable from TabButton to Tabs"""
        return self._parent.get_tab_var()

    def _get_button_names(self):
        """Gets the names of the buttons

        Arguments:
            None

        Returns:
            button_names (list[str])
                -- A list of names for the buttons
        """
        return []

    def _get_xml_cache(self, title):
        """Gets the relevant XML cache"""
        pass


class AddTab(Tab):
    """The Add Tab

    Inherits from Tab

    Methods:
        Overridden:
            _get_button_names() -> list[str]
                -- Gets the button name0s
            _get_xml_cache(title: str) -> xml.etree.ElementTree
                -- Gets the relevent XML cache
    """

    def _get_button_names(self):
        """Gets the button names

        Arguments:
            None

        Returns:
            button_names (list[str])
                -- The names of the buttons
        """

        # Return the keys (the titles for the field) from the relevent part of
        # XML Cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.add_cache.keys()

    def _get_xml_cache(self, title):
        """Gets the relevent xml cache with the title `title`

        Arguments:
            title (str)
                -- The title of the template cache

        Returns:
            template (xml.etree.ElementTree)
                -- The template cache
        """
        
        # Returns the relevent XML cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.add_cache[title]


class GetTab(Tab):
    """The Get Tab

    Inherits from Tab

    Methods:
        Overridden:
            _get_button_names() -> list[str]
                -- Gets the button name0s
            _get_xml_cache(title: str) -> xml.etree.ElementTree
                -- Gets the relevent XML cache
    """

    def _get_button_names(self):
        """Gets the button names

        Arguments:
            None

        Returns:
            button_names (list[str])
                -- The names of the buttons
        """

        # Return the keys (the titles for the field) from the relevent part of
        # XML Cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.get_cache.keys()

    def _get_xml_cache(self, title):
        """Gets the relevent xml cache with the title `title`

        Arguments:
            title (str)
                -- The title of the template cache

        Returns:
            template (xml.etree.ElementTree)
                -- The template cache
        """

        # Returns the relevent XML cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.get_cache[title]


class RemoveTab(Tab):
    """The Remove Tab

    Inherits from Tab

    Methods:
        Overridden:
            _get_button_names() -> list[str]
                -- Gets the button name0s
            _get_xml_cache(title: str) -> xml.etree.ElementTree
                -- Gets the relevent XML cache
    """

    def _get_button_names(self):
        """Gets the button names

        Arguments:
            None

        Returns:
            button_names (list[str])
                -- The names of the buttons
        """

        # Return the keys (the titles for the field) from the relevent part of
        # XML Cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.rem_cache.keys()

    def _get_xml_cache(self, title):
        """Gets the relevent xml cache with the title `title`

        Arguments:
            title (str)
                -- The title of the template cache

        Returns:
            template (xml.etree.ElementTree)
                -- The template cache
        """

        # Returns the relevent XML cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.rem_cache[title]


class ChangeTab(Tab):
    """The Change Tab

    Inherits from Tab

    Methods:
        Overridden:
            _get_button_names() -> list[str]
                -- Gets the button name0s
            _get_xml_cache(title: str) -> xml.etree.ElementTree
                -- Gets the relevent XML cache
    """

    def _get_button_names(self):
        """Gets the button names

        Arguments:
            None

        Returns:
            button_names (list[str])
                -- The names of the buttons
        """

        # Return the keys (the titles for the field) from the relevent part of
        # XML Cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.chg_cache.keys()

    def _get_xml_cache(self, title):
        """Gets the relevent xml cache with the title `title`

        Arguments:
            title (str)
                -- The title of the template cache

        Returns:
            template (xml.etree.ElementTree)
                -- The template cache
        """

        # Returns the relevent XML cache
        xml_cache = self._parent.get_xml_cache()
        return xml_cache.chg_cache[title]
