"""Various templates to be used in the tkinter"""

import tkinter as tk
import tkinter.font as tkfont

font = "TkFixedFont"


class Page(tk.Frame):
    """The base class for most custom widgets in this program.

    Inherits from tk.Frame.

    A page and all classes which inherit from it can only interact with their
    parent or their children

    Attributes:
        Protected:
            _parent (gui.templates.Page)
                -- The parent to this window

    Methods:
        Overriden:
            __init__(parent: gui.page.Page, *args, super_kwargs: dict, **kwargs) -> None
            __getattr__(name: str) -> Any

        Protected:
            _init_elements(*args, **kwargs) -> None
                -- Initilises the tkinter elements of the page
    """

    def __init__(self, parent, *args, super_kwargs=None, font=font, **kwargs):
        """The constructor for Page

        *args and **kwargs are passed to _init_elements

        Arguments:
            parent (gui.templates.Page)
                -- The parent to this window.

        Keyword Arguments:
            super_kwargs (dict)
                -- The keyword arguments to use in super().__init__
            font (str)
                -- The name of the font of the Page

        Returns:
            None
        """
        self._parent = parent

        # Make sure super_kwargs is a dictionary
        if super_kwargs is None:
            super_kwargs = {}
        super().__init__(parent, **super_kwargs)
        self.option_add("*Font", tkfont.nametofont(font))

        # Initilise the tkinter elements
        self._init_elements(*args, **kwargs)

    def _init_elements(self, *args, **kwargs):
        """Initilises and grids the tkinter elements."""
        pass

    def __getattr__(self, name):
        """Exists only to make HollowPage work"""
        return self.__getattribute__(name)


class HollowPage(Page):
    """A page where all attributes/methods are passed to the parent"""

    def __getattr__(self, name):
        """Gets an attribute if __getattribute__ does not find it"""
        return self._parent.__getattr__(name)


class HideablePage(Page):
    """A page which can be hidden. It must be gridded.

    Methods:
        show() -> None
            -- Shows the page
        hide() -> None
            -- Hides the page
    """

    def show(self):
        """Shows the page"""
        self.grid()

    def hide(self):
        """Hides the page"""
        self.grid_remove()


class Button(tk.Button):
    """A tkinter button.

    Inherits from tkinter.Button

    Attributes:
        Protected:
            _parent (gui.templates.Page)
                -- The parent to this window

    Methods:
        Overriden:
            __init__(parent: gui.page.Page, *args, super_kwargs: dict, **kwargs) -> None
            __getattr__(name: str) -> Any

        Protected:
            _init_elements(*args, **kwargs) -> None
                -- Initilises the tkinter elements of the button
            _get_text() -> str
                -- Gets the text used in the button
            _command() -> None
                -- The command when the button is pressed
    """

    def __init__(self, parent, *args, super_kwargs=None, font=font, **kwargs):
        """The constructor for Button

        *args and **kwargs are passed to _init_elements

        Arguments:
            parent (gui.templates.Page)
                -- The parent to this Button.

        Keyword Arguments:
            super_kwargs (dict)
                -- The keyword arguments to use in super().__init__
            font (str)
                -- The name of the font of the button

        Returns:
            None
        """
        self._parent = parent

        # Make sure that super_kwargs is a dict
        if super_kwargs is None:
            super_kwargs = {}

        # Set the text to what is returned by _get_text
        # and the command to _command
        super().__init__(
            parent,
            text=self._get_text(),
            command=self._command,
            font=tkfont.nametofont(font),
            **super_kwargs,
        )

        # Initilise the tkinter elements
        self._init_elements(*args, **kwargs)

    def _init_elements(self, *args, **kwargs):
        """Initilises the tkinter elements"""
        pass

    def _get_text(self):
        """The text used on the button

        Arguments:
            None

        Returns:
            text (str)
                -- The text used on the button
        """
        pass

    def _command(self):
        """The command when the button is pressed"""
        pass

    def __getattr__(self, name):
        """Exists only to make HollowPage work"""
        return self.__getattribute__(name)
