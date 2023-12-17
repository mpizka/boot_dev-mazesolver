#! /usr/bin/env python3
"""boot.dev Course 7 guided Project "Build a mazesolver"

This is a graphical mazesolver that generates and then solves 2D mazes with a
GUI based on the Tkinter library.

This is the main entry point and driver of the program.
"""

import random

from gui import Window
from geo import Point, Line, Cell


# run the application
if __name__ == "__main__":
    win = Window(800, 600)
    canvas = win.get_canvas()

    # Draw a couple of points
    for i in range(900):
        Point(
            300 + (10 * (i % 30)),
            100 + (10 * (i // 30)),
            random.choice(["red", "green", "blue", "grey"]),
        ).draw(canvas)

    # Draw a couple of Lines capped with points
    p1 = Point(100, 100)
    p2 = Point(200, 100)
    p3 = Point(100, 200)
    p4 = Point(200, 200)
    Line(p1, p4).draw(canvas)
    Line(p2, p3).draw(canvas)
    p1.draw(canvas)
    p2.draw(canvas)
    p3.draw(canvas)
    p4.draw(canvas)

    # cap the lines with cells forming corners
    Cell(Point(90, 90), Point(110, 110), r_wall=False, b_wall=False).draw(canvas)
    Cell(Point(190, 190), Point(210, 210), t_wall=False, l_wall=False).draw(canvas)
    Cell(Point(190, 90), Point(210, 110), l_wall=False, b_wall=False).draw(canvas)
    Cell(Point(90, 190), Point(110, 210), t_wall=False, r_wall=False).draw(canvas)

    # a path of cells left-right-down in inverted L shape
    path = [
        # left cap
        Cell(Point(100, 300), Point(120, 320), r_wall=False),
        # hallway
        Cell(Point(120, 300), Point(140, 320), l_wall=False, r_wall=False),
        Cell(Point(140, 300), Point(160, 320), l_wall=False, r_wall=False),
        Cell(Point(160, 300), Point(180, 320), l_wall=False, r_wall=False),
        Cell(Point(180, 300), Point(200, 320), l_wall=False, r_wall=False),
        # corner
        Cell(Point(200, 300), Point(220, 320), l_wall=False, b_wall=False),
        # down hallway
        Cell(Point(200, 320), Point(220, 340), t_wall=False, b_wall=False),
        Cell(Point(200, 340), Point(220, 360), t_wall=False, b_wall=False),
        Cell(Point(200, 360), Point(220, 380), t_wall=False, b_wall=False),
        Cell(Point(200, 380), Point(220, 400), t_wall=False, b_wall=False),
        # bottom cap
        Cell(Point(200, 400), Point(220, 420), t_wall=False),
    ]
    # draw the cells
    for cell in path:
        cell.draw(canvas)
    # draw the paths between them
    for i in range(len(path) - 1):
        path[i].draw_move(path[i + 1], i % 2 == 0).draw(canvas)

    win.wait_for_close()
