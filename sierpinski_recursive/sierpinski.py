"""
File: sierpinski.py
Name: Joanne Cho
---------------------------
This file recursively prints the Sierpinski triangle on GWindow.
The Sierpinski triangle is a fractal described in 1915 by Waclaw Sierpinski.
It is a self similar structure that occurs at different levels of iterations.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine
from campy.gui.events.timer import pause

# Constants
ORDER = 6                  # Controls the order of Sierpinski Triangle
LENGTH = 600               # The length of order 1 Sierpinski Triangle
UPPER_LEFT_X = 150		   # The upper left x coordinate of order 1 Sierpinski Triangle
UPPER_LEFT_Y = 100         # The upper left y coordinate of order 1 Sierpinski Triangle
WINDOW_WIDTH = 950         # The width of the GWindow
WINDOW_HEIGHT = 700        # The height of the GWindow

HEIGHT = 0.866
WIDTH = 0.5

# Global Variable
window = GWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # The canvas to draw Sierpinski Triangle


def main():
	"""
	Function: Create a Sierpinski Triangle by given ORDER.
	"""
	sierpinski_triangle(ORDER, LENGTH, UPPER_LEFT_X, UPPER_LEFT_Y)


def sierpinski_triangle(order, length, upper_left_x, upper_left_y):
	"""
	:param order: Controls the order of Sierpinski Triangle
	:param length: The length of order n Sierpinski Triangle
	:param upper_left_x: The upper left x coordinate of order n Sierpinski Triangle
	:param upper_left_y: The upper left y coordinate of order n Sierpinski Triangle
	:return: None
	"""
	if order == 0:		# Base Case
		pass
	else:
		# draw lines of Sierpinski Triangle
		line = GLine(upper_left_x, upper_left_y, upper_left_x + length, upper_left_y)
		window.add(line)
		line = GLine(upper_left_x, upper_left_y,  upper_left_x+length*WIDTH, upper_left_y+length*HEIGHT)
		window.add(line)
		line = GLine(upper_left_x+length, upper_left_y, upper_left_x+length*WIDTH, upper_left_y+length*HEIGHT)
		window.add(line)
		# do recursion
		sierpinski_triangle(order-1, length/2, upper_left_x, upper_left_y)
		sierpinski_triangle(order-1, length/2, upper_left_x+length/2, upper_left_y)
		sierpinski_triangle(order-1, length/2, upper_left_x+length/4, upper_left_y+((length*HEIGHT)/2))


if __name__ == '__main__':
	main()
