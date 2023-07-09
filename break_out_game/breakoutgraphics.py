"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
---------------------------
File: breakoutgraphics.py
Name: Joanne Cho
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
from campy.gui.events.timer import pause
from campy.graphics.gimage import GImage

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball

LOSER_FILEPATH = 'loser.jpg'
WINNER_FILEPATH = 'winner.jpg'
GAME_OVER_FILEPATH = 'game_over.jpg'
DELAY = 1000


class BreakoutGraphics:
    """
    Function: constructor of BreakoutGraphics class
    """
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # publish parameters
        self.__score = 0
        self.__lives = 0
        self.__switch = False
        self.__max_score = brick_rows * brick_cols
        self.__brick_rows = brick_rows
        self.__brick_cols = brick_cols
        self.__brick_width = brick_width
        self.__brick_height = brick_height
        self.__brick_offset = brick_offset
        self.__brick_spacing = brick_spacing

        # Create score label
        self.__score_label = GLabel("Score: " + str(self.__score))
        self.__score_label.font = '-15'
        self.window.add(self.__score_label, x=BRICK_SPACING, y=self.__score_label.height+BRICK_SPACING)

        # Create live label
        self.__live_label = GLabel("Lives: " + str(self.__lives))
        self.__live_label.font = '-15'
        self.window.add(self.__live_label, x=self.window.width - self.__live_label.width-BRICK_SPACING,
                        y=self.__live_label.height + BRICK_SPACING)

        # Create a paddle
        self.__paddle = GRect(width=PADDLE_WIDTH, height=PADDLE_HEIGHT)
        self.__paddle.filled = True
        self.window.add(self.__paddle, x=(self.window.width-self.__paddle.width)/2,
                        y=(self.window.height-PADDLE_OFFSET))

        # Center a filled ball in the graphical window, initialize position
        self.__ball = GOval(ball_radius*2, ball_radius*2)
        self.__ball.filled = True
        self.window.add(self.__ball, x=(self.window.width-self.__ball.width)/2,
                        y=(self.window.height-self.__ball.height)/2)

        # Initialize ball velocity
        self.__ball_dx = self.__ball_dy = 0             # Default velocity of ball
        self.__mouse_not_clicked = True                 # Default mouse-NOT-clicked flag

        # Create a brick wall
        self.create_bricks()

        # Initialize two mouse listeners
        onmousemoved(self.handle_paddle_move)
        onmouseclicked(self.initial_ball_velocity)

    def create_bricks(self):
        """
        Function: Create/Draw a brick wall
        :param: self.__brick_cols: number of bricks in a column
                self.__brick_rows: number of bricks in a row
        :return: none
        """
        for i in range(self.__brick_cols):
            for j in range(self.__brick_rows):
                tmp_brick = GRect(width=self.__brick_width, height=self.__brick_height)
                tmp_brick.filled = True
                if j in range(2):
                    tmp_brick.fill_color = 'red'
                elif j in range(4):
                    tmp_brick.fill_color = 'orange'
                elif j in range(6):
                    tmp_brick.fill_color = 'yellow'
                elif j in range(8):
                    tmp_brick.fill_color = 'green'
                elif j in range(10):
                    tmp_brick.fill_color = 'blue'
                self.window.add(tmp_brick, x=(i*(self.__brick_width+self.__brick_spacing)),
                                y=self.__brick_offset+(j*(self.__brick_height+self.__brick_spacing)))

    def reset_game(self):
        """
        Function: Reset ball and paddle position at center. Reset parameters.
        :param: none
        :return: none
        """
        self.__ball_dx = self.__ball_dy = 0
        self.__mouse_not_clicked = True
        self.__live_label.text = "Lives: " + str(self.__lives)
        self.__score_label.text = "Score: " + str(self.__score)
        self.window.add(self.__ball, x=(self.window.width-self.__ball.width)/2,
                        y=(self.window.height-self.__ball.height)/2)
        self.window.add(self.__paddle, x=(self.window.width-self.__paddle.width)/2,
                        y=(self.window.height-PADDLE_OFFSET))

    def handle_paddle_move(self, event):
        """
        Function: Handle paddle moving of "onmousemoved" event
        :param: none
        :return: none
        """
        dx = event.x - self.__paddle.width/2            # dx is at the center of paddle
        if dx < 0:                                      # fix left boundary of paddle
            dx = 0
        if dx > self.window.width-self.__paddle.width:  # fix right boundary of paddle
            dx = self.window.width-self.__paddle.width
        self.__paddle.x = dx                            # reset paddle x position. No need to change y position.

    def initial_ball_velocity(self, event):
        """
        Function: initial ball velocity of "onmouseclicked" event
        :param: none
        :return: none
        """
        self.__switch = True
        if self.__mouse_not_clicked:
            self.__mouse_not_clicked = False
            self.__ball_dy = INITIAL_Y_SPEED
            self.__ball_dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__ball_dx = -self.__ball_dx

    def handle_ball_hits_3_walls(self):
        """
        Function: Handler of a ball hits 3 walls(East, West and North)
                  When a ball hits a wall, bouncing back.
        :param: none
        :return: none
        """
        if self.__ball.x <= 0 or self.__ball.x + self.__ball.width >= self.window.width:
            self.__ball_dx = -self.__ball_dx
        if self.__ball.y <= 0:
            self.__ball_dy = -self.__ball_dy

    def is_ball_out_of_y_height(self):
        """
        Function: Is a ball out of Y-axis, which means checking if a ball moving beyond South wall.
        :param: none
        :return: True: When a ball moving beyond South wall.
        """
        out_of_y = False
        if self.__ball.y >= self.__ball.height + self.window.height:
            out_of_y = True
        return out_of_y

    def handle_ball_hits_object(self):
        """
        Function: Checking if a ball hits object.
                  - Hits Paddle object: bouncing back
                  - Hits Brick object: increase score, remove the brick, bouncing back
                  - Others: do nothing
        :param: none
        :return: none
        """
        # Key: 透過兩個 for loop 找到的四個點。
        hit = True
        for i in range(0, self.__ball.width*2, self.__ball.width):
            for j in range(0, self.__ball.width*2, self.__ball.width):
                probe = self.window.get_object_at(self.__ball.x+i, self.__ball.y+j)
                # Key: 因為球有四個偵測點，當某一點偵測到之後，設定flag，後續的偵測點就會略過。
                if hit:
                    if probe is not None and probe is not self.__score_label and probe is not self.__live_label:
                        if probe == self.__paddle:
                            if self.__ball_dy > 0:  # Avoid the ball sticking to the board
                                self.__ball_dy = -self.__ball_dy
                        else:
                            self.__ball_dy = -self.__ball_dy
                            self.window.remove(probe)
                            self.__score += 1
                            self.__score_label.text = "Score: " + str(self.__score)
                        hit = False

    def is_all_bricks_gone(self):
        """
        Function: Is all bricks gone
        :param: none
        :return: True: all bricks are cleared, which means user get maximum scores.
        """
        if self.__score < self.__max_score:
            return False
        else:
            return True

    def get_switch(self):
        """
        Function: Getter of switch
        :param: none
        :return: status of switch
        """
        return self.__switch

    def get_ball(self):
        """
        Function: Getter of ball object
        :param: none
        :return: ball object
        """
        return self.__ball

    def get_ball_dx(self):
        """
        Function: Getter of ball x velocity
        :param: none
        :return: ball x velocity
        """
        return self.__ball_dx

    def get_ball_dy(self):
        """
        Function: Getter of ball y velocity
        :param: none
        :return: ball y velocity
        """
        return self.__ball_dy

    def get_score(self):
        """
        Function: Getter of scores
        :param: none
        :return: scores
        """
        return self.__score

    def set_lives(self, x):
        """
        Function: Setter of game lives
        :param: lives
        :return: none
        """
        self.__lives = x
        self.__live_label.text = "Lives: " + str(self.__lives)

    def show_winner(self):
        """
        Function: Show winner picture
        :param: filepath of winning game image
        :return: none
        """
        img = GImage(WINNER_FILEPATH)
        self.window.add(img, (self.window.width - img.width)/2, (self.window.height - img.height)/2)
        pause(DELAY)
        self.window.remove(img)

    def show_looser(self):
        """
        Function: Show loser picture
        :param: filepath of losing game image
        :return: none
        """
        img = GImage(LOSER_FILEPATH)
        self.window.add(img, (self.window.width - img.width)/2, (self.window.height - img.height)/2)
        pause(DELAY)
        self.window.remove(img)

    def show_game_over(self):
        """
        Function: Show game-over picture
        :param: filepath of game-over image
        :return: none
        """
        img = GImage(GAME_OVER_FILEPATH)
        self.window.add(img, (self.window.width - img.width)/2, (self.window.height - img.height)/2)
        pause(DELAY)
