from graphics import Line, Point

class Cell:
    # Class which defines a cell. 
    # It should know which walls it has, where it exists on the canvas in x/y coordinates, and access to the window so that it can draw itself
    def __init__(self, window=None):
        # creates public methods which can be altered once a cell is create for existence of each wall
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        # initial cell does not have any coordinates until it needs to be draw
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        # establishes current window which the cell can be drawn on
        self._win = window
        self._visited = False

    def draw(self, x1, x2, y1, y2):
        # sets the x1, x2, y1, y2 attributes based on the coordinates given as argument which are then used to draw the cells
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        # create all the lines for a given cell
        left_wall = Line(Point(x1, y1), Point(x1, y2))
        right_wall = Line(Point(x2, y1), Point(x2, y2))
        top_wall = Line(Point(x1, y1), Point(x2, y1))
        bottom_wall = Line(Point(x1, y2), Point(x2, y2))
        # based on if the cell continues a left_wall, we draw or don't draw. repeats for each 
        if self.has_left_wall:
            self._win.draw(left_wall)
        else:
            self._win.draw(left_wall, fill_color="white")

        if self.has_right_wall:
            self._win.draw(right_wall)
        else:
            self._win.draw(right_wall, fill_color="white")

        if self.has_top_wall:
            self._win.draw(top_wall)
        else:
            self._win.draw(top_wall, fill_color="white")
        if self.has_bottom_wall:
            self._win.draw(bottom_wall)
        else:
            self._win.draw(bottom_wall, fill_color="white")

    # Draws a line from the center of one cell to another. color of the line changes depending on if undo is true or false
    # self is the original/starting cell and to_cell is the cell where the line will end up
    # center would be defined as a point halfway between x1, x2 and y1, y2
    def draw_move(self, to_cell, undo=False):
        center_line_color = "red"
        if undo:
            center_line_color = "gray"  
        # find the halfway point of the x and y coordinates of the self cell
        x_halfway_self = (self._x2 + self._x1) // 2
        y_halfway_self = (self._y2 + self._y1) // 2
        # find the halfway point of the x and y coordinates of the to_cell
        x_halfway_to_cell = (to_cell._x2 + to_cell._x1) // 2
        y_halfway_to_cell = (to_cell._y2 + to_cell._y1) // 2
        # create the line between the two cells and draw it based on the center_line_color
        path_line = Line(Point(x_halfway_self, y_halfway_self), Point(x_halfway_to_cell, y_halfway_to_cell))
        self._win.draw(path_line, center_line_color)
