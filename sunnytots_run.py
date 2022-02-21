import gui.master
import backend.master


def main():
    backend_master = backend.master.Backend()
    gui_master = gui.master.Gui(backend_master)
    gui_master.mainloop()


if __name__ == "__main__":
    main()
