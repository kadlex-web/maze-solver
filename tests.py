from maze import Maze
import unittest
import random

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_maze_create_cells2(self):
        num_cols = 20
        num_rows = 15
        m1 = Maze(50, 50, num_rows, num_cols, 20, 20)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_break_entrance_and_exit(self):
        num_cols = 4
        num_rows = 4
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall, 
            False,
        )
        self.assertEqual(
            m1._cells[num_cols-1][num_rows-1].has_bottom_wall,
            False,
        )

    def test_reset_cells_visited_method(self):
        num_cols = 20
        num_rows = 15
        m1 = Maze(50, 50, num_rows, num_cols, 20, 20)

        self.assertEqual(
            m1._cells[0][0]._visited, 
            False,
        )
        self.assertEqual(
            m1._cells[num_cols-1][num_rows-1]._visited,
            False,
        )
        rand_col = random.randrange(num_cols)
        rand_row = random.randrange(num_rows)
        self.assertEqual(
            m1._cells[rand_col][rand_row]._visited,
            False,
        )
if __name__ == "__main__":
    unittest.main()