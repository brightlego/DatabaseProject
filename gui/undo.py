import gui.templates


class UndoButton(gui.templates.Button):
    def _get_text(self):
        return "Undo"

    def _command(self):
        self._parent.undo()
