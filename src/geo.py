#! /usr/bin/env python3
"""boot.dev Course 7 guided Project "Build a mazesolver"

This is the geometry library for the project. It contains all forms that can be
drawn on the canvas provided by the gui. Each object is defined by a class, and
has a `draw()` method, which expects a tkinter canvas object as it's first
parameter.
"""

from dataclasses import dataclass
import tkinter as tk


@dataclass
class Point:
    """A point in a classic canvas-coordinate system.

    x=0, y=0 is the upper left corner

    I kinda changes this as well since I wanted to play around with the __add__
    semantics a little bit. Maybe a bit overengineered at this point.
    """

    x: int
    y: int
    color: str = "red"

    def draw(self, canvas: tk.Canvas):
        """Drawing a Point just adds a dot."""
        canvas.create_oval(
            self.x - 2,
            self.y - 2,
            self.x + 2,
            self.y + 2,
            fill=self.color,
        )

    def __add__(self, other):
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
    color: str = "black"
    width: int = 2

    def draw(self, canvas):
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=self.color,
            width=self.width,
        )


@dataclass
class Cell:
    """A cell on the mazes grid."""

    # top left & bottom right corners
    tl: Point
    br: Point

    # color
    color: str = "black"

    # walls
    l_wall: bool = True
    r_wall: bool = True
    t_wall: bool = True
    b_wall: bool = True

    def draw(self, canvas):
        """Draw cell to the windows canvas."""

        if self.l_wall:
            Line(self.tl, Point(self.tl.x, self.br.y), self.color).draw(canvas)
        if self.t_wall:
            Line(self.tl, Point(self.br.x, self.tl.y), self.color).draw(canvas)
        if self.r_wall:
            Line(self.br, Point(self.br.x, self.tl.y), self.color).draw(canvas)
        if self.b_wall:
            Line(self.br, Point(self.tl.x, self.br.y), self.color).draw(canvas)

    def center(self):
        """Returns the center of the cell as a Point."""
        center = Point(
            self.tl.x + (self.br.x - self.tl.x) / 2,
            self.tl.y + (self.br.y - self.tl.y) / 2,
        )
        return center

    def draw_move(self, to_cell, undo=False):
        """Returns a path between the centers of 2 cells as a `Line`.

        The line is grey if undo is True, red otherwise.
        """
        return Line(self.center(), to_cell.center(), "grey" if undo else "red")
