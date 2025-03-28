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
        if seed:
            random.seed(seed)
        # Generate the cell structure of the maze
        self._create_cells()
        # Create the entrance and the exit
        self._break_entrance_and_exit()
        # build a maze!
        self._break_walls_r(0,0)
        # reset visited property of all cells so that solve can be called on the maze
        self._reset_cells_visited()

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
    
    def _reset_cells_visited(self):
        for i in range(len(self._cells)): 
            for j in range(len(self._cells[i])):
                # call the _draw_cell method on the cell object
                self._cells[i][j]._visited = False

    def _break_walls_r(self, i, j):
        print(f'im in ({i},{j})')
        # Marks the current cell as visited
        self._cells[i][j]._visited = True
        visiting = True

        # create a to_visit dict which stores possible neighbors that can be visited
        while visiting:
            to_visit = self._generate_unvisited_neighbors(i,j)

            # If the to_visit dict has values selects a random one and recursively calls break walls
            if len(to_visit) > 0:
                # Picking a random direction
                n = random.randrange(len(to_visit))
                next = list(to_visit)[n]
                to_cell_break = to_visit[next]["cell"]
                # breaking the wall
                if next == "top":
                    print('breaking top wall')
                    to_cell_break.has_bottom_wall = False
                    self._draw_cell(to_visit[next]["coordinates"][0], to_visit[next]["coordinates"][1])
                    self._cells[i][j].has_top_wall = False
                    self._draw_cell(i, j)
                elif next == "bottom":
                    print('breaking bottom wall')
                    to_cell_break.has_top_wall = False
                    self._draw_cell(to_visit[next]["coordinates"][0], to_visit[next]["coordinates"][1])           
                    self._cells[i][j].has_bottom_wall = False
                    self._draw_cell(i,j)                    
                elif next == "left":
                    print('breaking left wall')
                    to_cell_break.has_right_wall = False
                    self._draw_cell(to_visit[next]["coordinates"][0], to_visit[next]["coordinates"][1])                        
                    self._cells[i][j].has_left_wall = False
                    self._draw_cell(i,j)                         
                elif next == "right":
                    print('breaking right wall')
                    to_cell_break.has_left_wall = False
                    self._draw_cell(to_visit[next]["coordinates"][0], to_visit[next]["coordinates"][1])                        
                    self._cells[i][j].has_right_wall = False
                    self._draw_cell(i,j)                         
                print(f'moving to: {to_visit[next]["coordinates"]}')
                self._break_walls_r(to_visit[next]["coordinates"][0], to_visit[next]["coordinates"][1])

            else:
                # print("No unvisited neighbors -- reversing course")
                # Draws the current cell and exits the current iteration of the loop
                self._draw_cell(i, j)
                return
            
    # Helper method which generates unvisited_neighbors for both _break_walls_r and _solve_r     
    def _generate_unvisited_neighbors(self, i, j):
        to_visit = {}
        adj_neighbors = {
            "top": (0, -1), 
            "bottom": (0, 1), 
            "left": (-1, 0), 
            "right": (1, 0),
            }
        for key in adj_neighbors:
            if i + adj_neighbors[key][0] < 0 \
                or i + adj_neighbors[key][0] > (self.num_cols - 1)\
                or j + adj_neighbors[key][1] < 0 \
                or j + adj_neighbors[key][1] > (self.num_rows - 1):
                    pass
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
        return to_visit
    
    def solve(self):
        print("\n\n")
        print("------Starting Solver------")
        # Calls the recursively solve on the starting cell (0,0)
        # Returns true if the maze can be solved, otherwise False
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        # animate the cell
        self._animate()
        # mark the cell as visited
        self._cells[i][j]._visited = True
        # if the i is equal to cols number, and j is equal to the rows number - we've reach the exit!
        if self.num_cols - 1 == i and self.num_rows - 1 == j:
            print("im at the finish")
            return True
        else:
            # Generate valid neighbors which can be visited (they haven't previously been visited)
            unvisited = self._generate_unvisited_neighbors(i, j)
            if len(unvisited) > 0:
                for neighbor in unvisited:
                    print(neighbor)
                    to_cell = unvisited[neighbor]["cell"]
                    print(unvisited[neighbor]["coordinates"])

                    if neighbor == "top":
                        print("moving up")
                        if to_cell.has_bottom_wall == False and self._cells[i][j].has_top_wall == False:
                            print("moving up 2")
                            self._cells[i][j].draw_move(to_cell)
                            if self._solve_r(i, j-1) == True:
                                return True
                            else:
                                self._cells[i][j].draw_move(to_cell, undo=True)

                    elif neighbor == "bottom":
                        print("moving down")
                        print(to_cell.has_top_wall)
                        print(self._cells[i][j].has_bottom_wall)
                        if to_cell.has_top_wall == False and self._cells[i][j].has_bottom_wall == False:
                            print("moving down 2")
                            self._cells[i][j].draw_move(to_cell)
                            if self._solve_r(i, j+1) == True:
                                return True
                            else:
                                self._cells[i][j].draw_move(to_cell, undo=True)                           
                    elif neighbor == "left":
                        print("moving left")
                        if to_cell.has_right_wall == False and self._cells[i][j].has_left_wall == False:
                            print("moving left 2")
                            self._cells[i][j].draw_move(to_cell)
                            if self._solve_r(i-1, j) == True:
                                return True
                            else:
                                self._cells[i][j].draw_move(to_cell, undo=True)                           
                    elif neighbor == "right":
                        print("moving right")
                        print(to_cell.has_left_wall)
                        print(self._cells[i][j].has_right_wall)
                        if to_cell.has_left_wall == False and self._cells[i][j].has_right_wall == False:
                            print("moving right 2")
                            self._cells[i][j].draw_move(to_cell)
                            if self._solve_r(i+1, j) == True:
                                return True
                            else:
                                self._cells[i][j].draw_move(to_cell, undo=True)                            
                return False