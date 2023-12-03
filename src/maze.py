#! /usr/bin/env python3
"""boot.dev Course 7 guided Project "Build a mazesolver"

This is a graphical mazesolver that generates and then solves 2D mazes with a
GUI based on the Tkinter library.
"""

from dataclasses import dataclass
from tkinter import Tk, BOTH, Canvas


@dataclass
class Point:
    """A point in a classic canvas-coordinate system.

    x=0, y=0 is the upper left corner
    """

    x: int = 0
    y: int = 0


@dataclass
class Line:
    """A line between two points in a classic canvas-coordinate system."""

    p1: Point
    p2: Point
    fill_color: str
    width: int = 2


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

    def redraw(self):
        """Does a single redraw."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """Replaces mainloop() for our app."""
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        """Handler for WM_DELETE_WINDOW protocol."""
        self.__running = False

    def draw_line(self, line: Line):
        """Draw an instance of Line on the canvas.

        I changed this from the example, because it makes more sense to me,
        semantically to have the drawing logic on the window instead of the
        Line.
        """
        self.__canvas.create_line(
            line.p1.x,
            line.p1.y,
            line.p2.x,
            line.p2.y,
            fill=line.fill_color,
            width=line.width,
        )


# run the application
if __name__ == "__main__":
    win = Window(800, 600)
    win.draw_line(Line(Point(0, 0), Point(100, 100), "red"))
    win.draw_line(Line(Point(100, 0), Point(0, 100), "red"))
    win.wait_for_close()
