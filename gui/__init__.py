# Import only the GUI class from the file gui/master.py to prevent
# sunnytots_run.py having too much access to various elements

from gui.master import Gui

print(f"Initilising GUI {Gui}")
