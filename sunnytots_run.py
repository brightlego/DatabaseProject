import gui
import backend


def main():
    backend_master = backend.Backend()
    gui_master = gui.Gui(backend_master)
    gui_master.mainloop()


if __name__ == "__main__":
    main()
