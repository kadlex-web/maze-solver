from graphics import Window, Line, Point, Cell

def main():
    window = Window(800, 600)

    cell1 = Cell(window)
    cell1.has_bottom_wall = False
    cell1.has_top_wall = False
    cell1.draw(100, 200, 200, 300)

    cell2 = Cell(window)
    cell2.has_right_wall = False
    cell2.has_left_wall = False
    cell2.draw(200, 300, 300, 400)

    window.wait_for_close()

main()