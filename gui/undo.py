"""This file contains the class used in the undo button"""

import gui.templates
import tkinter as tk


class UndoButton(gui.templates.Button):
    """The undo button.

    Inherits from gui.templates.Button

    Methods:
        Overriden:
            _get_text() -> str
                -- Gets the text for the button
            _command() -> None
                -- Runs when the button is pressed
    """

    def _get_text(self):
        """Gets the text for the button"""
        return "Undo the Previous Change"

    def _command(self):
        """Runs the command when the button is pressed"""

        answer = tk.messagebox.askyesno(
            "Undoing previous change",
            "Are you sure you want to undo the previous change to the database?",
        )
        if answer == tk.messagebox.YES:
            # Undoes the previous change.
            self._parent.undo()
