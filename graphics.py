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

    def draw(self, line, fill_color):
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

    # takes the values of the points and then draws a line between the two of them...I think?
    def draw(self,canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
)