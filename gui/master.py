"""The master for the GUI.

It should not be imported directly. It should be accessed externally only with
`import gui`. Then `gui.Gui` should give the Gui class.
"""

# Import various tkinter stuff
import tkinter as tk
import tkinter.messagebox as tkmessagebox
from tkinter import ttk
import sqlite3

# Import all the widgets in from the different files in the gui
import gui.templates
import gui.tabs
import gui.input.input_field
import gui.tabbar
import gui.input.input_xml_cache
import gui.undo
import gui.output


class Gui(gui.templates.Page):
    """The main class for the GUI.
    Inherits from the basic 'Page' template. See gui/templates.py for more info.

    Attributes:
        Public:
            None
        Private:
            __backend (backend.master.Backend)
                -- The master for the backend. Handles queries.
            __root (gui.master.GuiRoot)
                -- The root of the Gui.
            __xml_cache (gui.input.input_xml_cache.XmlCache)
                -- A cache of all the parsed XML data for the structure of the
                   input field
            __input_is_empty (bool)
                -- Whether the input field is empty for use in hiding the input
                   field.
        Tkinter Elements:
            __tabbar (gui.tabbar.TabBar)
                -- The bar which holds the buttons to visit the various tabs
                   for the input field
            __tabs (gui.tabs.Tabs)
                -- The various tabs which decide the input field
            __input (gui.input.input_field.InputField)
                -- The field in which the input exists
            __output (gui.output.OutputBox)
                -- The box which holds the output from the queries
            __undo_button (gui.undo.UndoButton)
                -- The undo button

    Methods:
        Overriden:
            __init__(backend: backend.master.Backend) -> None

            _init_elements() -> None
                -- Initilises the tkinter elements

        Public:
            get_xml_cache() -> gui.input.input_xml_cache.XMLCache
                -- Accessor for the XML Cache
            change_tab(tab: str) -> None
                -- Changes the tab to the tab specified by `tab`
            change_input(template: xml.etree.ElementTree) -> None
                -- Changes the input field to the one specified by `template`
            gen_new_query(type_: str) -> backend.query.Query
                -- Generates a new query as speficied by `type_`
            submit_query(query: backend.query.Query) -> None
                -- Submits a query to the backend for execution
            commit() -> None
                -- Commits the changes to the database
            rollback() -> None
                -- Rolls back the changes to the database to the last commit
            close() -> None
                -- Closes the database
            undo() -> None
                -- Undoes the previous change to the database
            mainloop() -> None
                -- Runs the mainloop of the tkinter root
    """

    def __init__(self, backend):
        """Initilises the GUI

        Arguments:
            backend (backend.master.Backend)
                -- The backend for the database
        Returns:
            None
        """
        self.__backend = backend  # The backend
        self.__root = GuiRoot(self)  # Generates the root of the program

        # Generates a cache for the xml data to format the input field
        self.__xml_cache = gui.input.input_xml_cache.XMLCache()

        super().__init__(self.__root)

    def _init_elements(self):
        """Initilises the elements of the GUI

        Arguments:
            None
        Returns:
            None
        """
        # The bar which selects which tab
        self.__tabbar = gui.tabbar.TabBar(self)

        # The tab
        self.__tabs = gui.tabs.Tabs(self)

        # The input field
        self.__input = gui.input.input_field.InputField(self)

        # Whether the input field is empty.
        self.__input_is_empty = True

        # The output box
        self.__output = gui.output.OutputBox(self)

        # The undo button
        self.__undo_buton = gui.undo.UndoButton(self)

        # Create seperators between the TabBar and the Tabs; between
        # the Tabs and the InputField and between the InputField and the
        # OutputBox respectively
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=2, columnspan=100, sticky=tk.EW
        )
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=4, columnspan=100, sticky=tk.EW
        )
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            column=0, row=6, columnspan=100, sticky=tk.EW
        )

        # Grid the elements where they are sticky to the west
        self.__tabbar.grid(column=0, row=0, sticky=tk.W)
        self.__tabs.grid(column=0, row=1, pady=5, sticky=tk.W)
        self.__input.grid(column=0, row=3)
        self.__undo_buton.grid(column=0, row=5, sticky=tk.W)
        self.__output.grid(column=0, row=7)

        # Ungrid the input as it is empty. It will be regridded when it is not
        # emtpy
        self.__input.grid_remove()

        # Clear the tabs for the time being
        self.change_tab()

        # Pack the Gui into the root
        self.pack(expand=True, fill=tk.BOTH)

    def get_xml_cache(self):
        """Accessor for the XML Cache

        Arguments:
            None

        Returns:
            xml_cache (gui.input.input_xml_cache.XMLCache)
                -- The XML Cache
        """
        return self.__xml_cache

    def change_tab(self, tab=None):
        """Changes the tabs to `tab`

        Arguments:
            None

        Keyword Arguments:
            tab (str)
                -- The tab to change to
        """

        # Pass the request onto tabs
        self.__tabs.change_tab(tab)

    def change_input(self, template):
        """Changes the input to the one specified in `template`

        Arguments:
            template (xml.etree.ElementTree)
                -- The XML template for the input

        Returns:
            None
        """

        # If the input is empty, grid it and set __input_is_empty to True
        if self.__input_is_empty:
            self.__input.grid()
        self.__input_is_empty = False

        # Set the input field to the template
        self.__input.set_template(template)

    def gen_new_query(self, type_, limit):
        """Get a new query of type `type_`

        Arguments:
            type_ (str)
                -- The type of query
            limit (int)
                -- The limit of the query

        Returns:
            query (backend.query.Query)
                -- The empty query
        """
        # Get the query from the backend
        return self.__backend.gen_new_query(type_, limit)

    def submit_query(self, query):
        """Submits a query to the backend and handles the output

        Arguments:
            query (backend.query.Query)
                -- The query

        Returns:
            None
        """
        fields = query.get_fields()
        try:
            data = self.__backend.handle_query(query)

        # Check if a UNIQUE constraint has failed and give an appropriate error
        except sqlite3.IntegrityError as err:
            self.__output.reset()
            if err.args[0].startswith("UNIQUE constraint failed"):
                self.__output.set_headers({"ERROR: Already Exists": [""]})
        if fields:
            self.__output.reset()
            self.__output.set_headers(fields)
            self.__output.set_data(data)

    def commit(self):
        """Commits the changes to the database so far

        Arguments:
            None

        Returns:
            None
        """
        self.__backend.commit()

    def rollback(self):
        """Rolls back the changes to the database to the previous commit

        Arguments:
            None

        Returns:
            None
        """
        self.__backend.rollback()

    def undo(self):
        """Undoes the previous change to the database

        Arguments:
            None

        Returns:
            None
        """
        self.__backend.undo()

    def mainloop(self, *args, **kwargs):
        """Runs the mainloop of the root."""
        self.__root.mainloop(*args, **kwargs)

    def close(self):
        """Close the database"""
        self.__backend.close()


class GuiRoot(tk.Tk):
    """The root for the GUI.

    Inherits from tkinter.Tk

    Attributes:
        Public:
            None
        Private:
            __gui (gui.master.Gui)
                -- The gui this root is in.

    Methods:
        Overriden:
            __init__(gui: gui.master.Gui) -> None

            destroy() -> None
                -- Handles whether to save or not when attempting to destroy
                   the window.
    """

    def __init__(self, gui):
        """The constructor for GuiRoot

        Arguments:
            gui (gui.master.Gui)
                -- The gui instance this is the root of

        Returns:
            None
        """
        # Save the gui
        self.__gui = gui
        super().__init__()

    def destroy(self):
        """The destructor for GuiRoot.

        Arguments:
            None

        Returns:
            None
        """

        # Ask if the user wants to save changes to the database
        answer = tkmessagebox.askyesnocancel(
            title="Exiting", message="Do you want to save changes to the database?"
        )

        # If the user answers cancel, abort destruction
        if answer is None:
            return

        # If the user answers yes, commit changes to the database and
        # destroy self
        elif answer:
            self.__gui.commit()

        # If the user answers no, rollback changes to the database and
        # destroy self
        else:
            self.__gui.rollback()

        # Close the database
        self.__gui.close()
        super().destroy()
