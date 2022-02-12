import gui.master
import backend.master

def main():
    backend_master = backend.master.Backend()
    gui_master = gui.maser.Gui(backend_master)
    gui_maser.mainloop()