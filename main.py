from graphics import Window, Line, Point

def main():
    window = Window(800, 600)
    line1 = Line(Point(100,200), Point(200,300))
    line2 = Line(Point(400,400), Point(100,100))
    window.draw(line1, "black")
    window.draw(line2, "blue")
    window.wait_for_close()

main()