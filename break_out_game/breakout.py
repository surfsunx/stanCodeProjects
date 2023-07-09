"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
---------------------------
File: breakout.py
Name: Joanne Cho
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second  # 10
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()                   # call constructor
    lives = NUM_LIVES                               # initial number of lives
    graphics.set_lives(lives)                       # create live label object

    # Add the animation loop here!
    while True:
        if graphics.get_switch():
            if graphics.is_all_bricks_gone():       # check if all bricks gone
                graphics.show_winner()              # show winner picture
                break                               # When user win, end this game.

            if graphics.is_ball_out_of_y_height():  # if ball moving beyond south wall
                lives -= 1                          # decrease one live
                graphics.set_lives(lives)
                if lives > 0:                       # if there are still lives
                    graphics.show_looser()          # show loser picture
                    graphics.reset_game()           # reset game
                else:
                    graphics.show_game_over()       # no available lives
                    break                           # Exit animation loop

            # handle ball moving
            graphics.get_ball().move(graphics.get_ball_dx(), graphics.get_ball_dy())

            # handle ball hit 3 walls
            graphics.handle_ball_hits_3_walls()

            # handle ball hits objects. Remove brick objects when ball is moving.
            if graphics.get_ball_dx() != 0 and graphics.get_ball_dy() != 0:
                graphics.handle_ball_hits_object()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
