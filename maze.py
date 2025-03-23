import time
import random
from cell import Cell

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._seed = seed
        # Generate the cell structure of the maze
        self._create_cells()
        # Create the entrance and the exit
        self._break_entrance_and_exit()
        # build a maze!
        self._break_walls_r(0,0)

    def _create_cells(self):
        for _ in range(self.num_cols):
            sub_list = []
            for _ in range(self.num_rows):
                c = Cell(self._win)
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
        if self._win is None:
            return
        c = self._cells[i][j]
        x1 = self.x1 + (i * self.cell_size_x)
        y1 = self.y1 + (j * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        c.draw(x1, x2, y1, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # Entrance is always the top wall in the top-left cell
        # in self._cells this would be self._cells[0][0]
        # exit is always the bottom wall in the bottom-right cell
        # in self._cells this would be self._cells[length of cols -1][length of rows-1]
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(0,0)
        exit = self._cells[self.num_cols - 1][self.num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)
    
    def _break_walls_r(self, i, j):
        print(f'im in ({i},{j})')
        # Marks the current cell as visited
        self._cells[i][j]._visited = True
        visiting = True
        adj_neighbors = {
            "top": (0, -1), 
            "bottom": (0, 1), 
            "left": (-1, 0), 
            "right": (1, 0),
            }
        # create a to_visit dict which stores possible neighbors that can be visited
        while visiting:
            to_visit = {}
            '''The for loop helps build out a list of neighbors which can be visited - could be written as a function block for cleaner code in this function'''
            # use the adjacent neighbors dict to check if a neighbor actually exists
            for key in adj_neighbors:
                if i + adj_neighbors[key][0] < 0 \
                    or i + adj_neighbors[key][0] > (self.num_rows - 1)\
                    or j + adj_neighbors[key][1] < 0 \
                    or j + adj_neighbors[key][1] > (self.num_cols - 1):
                        print("out of bounds")
                # If the neighbor exists -- store its coordinates and create a reference to that cell
                else:
                    neighbor_coordinates = (i + adj_neighbors[key][0], j + adj_neighbors[key][1])
                    neighbor_cell = self._cells[neighbor_coordinates[0]][neighbor_coordinates[1]]
                    # If the cell hasn't been visited before -- we can add it to a list of neighbors which can be visited from this cell
                    if neighbor_cell._visited == False:
                        to_visit[key] = {
                            "cell" : neighbor_cell,
                            "coordinates" : neighbor_coordinates,
                        }
            # If the to_visit dict has values selects a random one and recursively calls break walls
            print(to_visit)
            if len(to_visit) > 0:
                # Picking a random direction
                n = random.randrange(len(to_visit))
                next = list(to_visit)[n]
                # breaking the wall
                if next == "top":
                    print('breaking top wall')
                    to_visit[next]["cell"].has_top_wall == False
                elif next == "bottom":
                    print('breaking bottom wall')
                    to_visit[next]["cell"].has_bottom_wall == False
                elif next == "left":
                    print('breaking left wall')
                    to_visit[next]["cell"].has_left_wall == False
                elif next == "right":
                    print('breaking right wall')
                    to_visit[next]["cell"].has_right_wall == False
                print(f'moving to {next}: {to_visit[next]["coordinates"]}')
                self._break_walls_r(to_visit[next]["coordinates"][0], to_visit[next]["coordinates"][1])

            else:
                print("No unvisited neighbors -- reversing course")
                # Draws the current cell and exits the current iteration of the loop
                self._draw_cell(i, j)
                return