from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height): 
        self.height = height
        self.width = width
        self.__root = Tk() # creates a root widget
        self.__root.title("Maze Solver!") # gives the root widget a title
        self.canvas = Canvas(master=self.__root, height=self.height, width=self.width, bg="white") # creates a canvas widget
        self.canvas.pack() # packs the canvas widget so it can be loaded
        self.is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()
        print("closing the window")

    def close(self):
        self.is_running = False

    def draw(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    # constructor requires a two points which can be accessed later
    def __init__(self, point1, point2):
        self.point1 = point1 # first point object
        self.point2 = point2 # second point object

    # takes the values of the points and then draws a line between the two of them
    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

class Cell:
    # Class which defines a cell. 
    # It should know which walls it has, where it exists on the canvas in x/y coordinates, and access to the window so that it can draw itself
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = window

    def draw(self, x1, x2, y1, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            left_wall = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw(left_wall)

        if self.has_right_wall:
            right_wall = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw(right_wall)

        if self.has_top_wall:
            top_wall = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw(top_wall)

        if self.has_bottom_wall:
            bottom_wall = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw(bottom_wall)

'''
(1,1)      (2,1)

(1,2)      (2,2)
'''