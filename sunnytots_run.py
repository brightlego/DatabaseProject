"""Run this file to run the application

Usage:
    Linux:
        python3 sunnytots_run.py
    Windows/MacOS:
        python sunnytots_run.py
"""

# Import __init__ from the GUI and the backend
import gui
import backend


def main():
    # Create the backend
    backend_master = backend.Backend()

    # Create the GUI with reference to the backend
    gui_master = gui.Gui(backend_master)

    # Run the GUI
    gui_master.mainloop()


if __name__ == "__main__":
    main()
