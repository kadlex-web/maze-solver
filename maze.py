import time
from graphics import Cell, Window

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for _ in range(self.num_rows):
            sub_list = []
            for _ in range(self.num_cols):
                c = Cell(self.win)
                sub_list.append(c)
            self._cells.append(sub_list)

        # Now that the matrix is built we need to draw some cells!
        for i in range(len(self._cells)): 
            for j in range(len(self._cells[i])):
                # call the _draw_cell method on the cell object
                self._draw_cell(i,j)

    def _draw_cell(self, i, j):
        # if we take the starting x and starting y -- we are able to find the cell coordinates by multiplying i by cell_size x and j by cell_size y and 
        # adding them to the x1 and y1 of the maze (which is the starting point)
        # for example if the starting points is 100,100 -- and each cell is 100x100 then we know the first cell would be at
        # 100, 200, 100, 200. if we add i * cell_size_x -- which in this case is 100 and do the same for i * cell_size_y to the starting x1,y1
        # 200, 300, 200, 300 would be the next cell
        c = self._cells[i][j]
        x1 = self.x1 + (i * self.cell_size_x)
        y1 = self.y1 + (j * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        c.draw(x1, x2, y1, y2)
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)