#! /usr/bin/env python3
"""boot.dev Course 7 guided Project "Build a mazesolver"

This module holds the maze-class of our program.
"""

from gui import Window
from geo import Point, Line, Cell


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.win: Window = win

        self._cells: list[list[Cell]] = []
        self._create_cells()

    def _create_cells(self):
        cur_orig = Point(self.x1, self.y1)

        for c in range(self.num_cols):
            cur = cur_orig + (self.cell_size * c, 0)
            col = []
            for r in range(self.num_rows):
                print(cur)
                cell = Cell(cur, cur + (self.cell_size, self.cell_size))
                col.append(cell)
                cur = cur + (0, self.cell_size)
            self._cells.append(col)

    def draw_all_cells(self):
        canvas = self.win.get_canvas()
        for col in self._cells:
            for cell in col:
                cell.draw(canvas)
