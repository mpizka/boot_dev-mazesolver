#! /usr/bin/env python3
"""boot.dev Course 7 guided Project "Build a mazesolver"

This is a graphical mazesolver that generates and then solves 2D mazes with a
GUI based on the Tkinter library.
"""

from dataclasses import dataclass
from tkinter import Tk, BOTH, Canvas

from typing import Self
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

    def draw_line(self, line: "Line"):
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


@dataclass
class Point:
    """A point in a classic canvas-coordinate system.

    x=0, y=0 is the upper left corner

    I kinda changes this as well since I wanted to play around with the __add__
    semantics a little bit. Maybe a bit overengineered at this point.
    """

    x: int
    y: int

    def __add__(self, other: tuple[int, int] | Self):
        """Add a tuple (int,int) or another point to a point."""
        if isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError(
            "unsupported operand type(s) for +: "
            f"'{self.__class__.__name__}' and '{other.__class__.__name__}'"
        )


@dataclass
class Line:
    """A line between two points in a classic canvas-coordinate system."""

    p1: Point
    p2: Point
    fill_color: str
    width: int = 2


@dataclass
class Cell:
    """A cell on the mazes grid."""

    # window referenc
    win: Window
    # top left corner coordinates
    top_left: Point
    # walls
    has_left_wall: bool = True
    has_right_wall: bool = True
    has_top_wall: bool = True
    has_bottom_wall: bool = True
    # edge length
    edge: int = 20

    def draw(self):
        """Draw cell to the windows canvas."""
        tl = self.top_left
        w = self.edge
        c = "black"

        if self.has_left_wall:
            self.win.draw_line(Line(tl, tl + (0, w), c))
        if self.has_top_wall:
            self.win.draw_line(Line(tl, tl + (w, 0), c))
        if self.has_right_wall:
            self.win.draw_line(Line(tl + (w, 0), tl + (w, w), c))
        if self.has_bottom_wall:
            self.win.draw_line(Line(tl + (0, w), tl + (w, w), c))

    def draw_move(self, to_cell, undo=False):
        other_center = Point(
            to_cell.top_left.x + to_cell.edge / 2,
            to_cell.top_left.y + to_cell.edge / 2,
        )
        center = Point(
            self.top_left.x + self.edge / 2,
            self.top_left.y + self.edge / 2,
        )
        line = Line(center, other_center, "grey" if undo else "red")
        self.win.draw_line(line)


# run the application
if __name__ == "__main__":
    win = Window(800, 600)

    # first couple draw tests
    win.draw_line(Line(Point(100, 100), Point(200, 200), "red"))
    win.draw_line(Line(Point(200, 100), Point(100, 200), "red"))
    Cell(win, Point(90, 90)).draw()
    Cell(win, Point(190, 190), has_left_wall=False).draw()
    Cell(win, Point(190, 90), has_right_wall=False, has_left_wall=False).draw()
    Cell(win, Point(90, 190), has_top_wall=False, has_bottom_wall=False).draw()

    # small grid draw test
    grid_cells = []
    top_left = Point(400, 60)
    n_cells = 64
    cells_per_row = 4
    for i in range(n_cells):
        c = Cell(win, top_left + (20 * (i % cells_per_row), 20 * (i // cells_per_row)))
        grid_cells.append(c)
        c.draw()
    for i in range(len(grid_cells) - 1):
        grid_cells[i].draw_move(grid_cells[i + 1], bool(i % 2))

    win.wait_for_close()
