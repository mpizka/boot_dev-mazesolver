"""boot.dev Course 7 guided Project "Build a mazesolver"

This is the gui library of this project. It contains the tkinter specific
elements, that is: The window class which will serve as the basis for the GUI.
"""

from tkinter import Tk, BOTH, Canvas

import time


class Window:
    """Represents the Application windows.

    Since our App will take control of the update processes, this will include
    methods replacing mainloop() as well as a custom binding to the
    WM_DELETE_WINDOW window manager protocol.
    """

    def __init__(self, width, height):
        """Initialize the window with given width and height."""
        # track application running state
        self.__running = False

        # define root container
        self.__root = Tk()
        self.__root.title("Mazesolver")
        self.__root.geometry(f"{width}x{height}")
        # bind our custom close method to the window managers close
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        # define canvas
        self.__canvas = Canvas(
            master=self.__root,  # which container widget does this belong to
            width=width,
            height=height,
            bg="white",
        )
        # allow the canvas to expand and fill unsued space
        self.__canvas.pack(
            fill=BOTH,
            expand=True,
        )

    # Our app will take care of redrawing by itselfinstead of using a
    # mainloop(), so we need functions for update/redraw and waiting for the
    # close signal from the window manager (WM)

    def redraw(self):
        """Does a single redraw."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """Replaces mainloop() for our app."""
        self.__running = True
        while self.__running:
            self.redraw()
            # rate limited so the CPU doesn't go crazy during tests
            time.sleep(0.1)

    def close(self):
        """Handler for WM_DELETE_WINDOW protocol."""
        self.__running = False

    def get_canvas(self):
        """Return a reference to the GUI's canvas object."""
        return self.__canvas
