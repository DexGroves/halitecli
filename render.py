#!/usr/bin/env python

"""http://gnosis.cx/publish/programming/charming_python_6.html"""


import curses
import traceback
import numpy as np
import halite_cli as hlt


replay = hlt.Replay("hlt/blueonblue.hlt")  # TODO: argparse this


def stack_map(board):
    strength = board["strength"]
    owner = board["owner"]
    production = board["production"]

    return np.stack([production, strength, owner], axis=2).astype(int)


def format_as_fraction(element):
    numerator = justify_int(element[1], 3, 'right')
    denominator = justify_int(element[0], 2, 'left')
    str_ = numerator + '/' + denominator
    return str_


def justify_int(element, to, how='left'):
    s = str(element)
    if how == 'left':
        return s + ' ' * (to - len(s))
    if how == 'right':
        return ' ' * (to - len(s)) + s


def main(stdscr):
    # Frame the interface area at fixed VT100 size
    current_frame = 0
    board = replay.map_at(current_frame)

    global screen
    screen = stdscr.subwin(board['height'] + 2, board['width'] * 6 + 2, 0, 0)
    screen.box()
    # screen.hline(2, 1, curses.ACS_HLINE, 77)
    screen.refresh()

    keypress = ''
    while keypress != ord('q'):
        board = replay.map_at(current_frame)
        stacked = stack_map(board)
        fractions = np.apply_along_axis(format_as_fraction, 2, stacked).T
        colors = stacked[:, :, 2].T
        for x in range(fractions.shape[0]):
            for y in range(fractions.shape[1]):
                color = colors[x, y]
                stdscr.addstr(y + 1, x * 6 + 1, fractions[x, y],
                              curses.color_pair(color + 1))
        keypress = stdscr.getch()

        if keypress == curses.KEY_LEFT:
            current_frame = max(0, current_frame - 1)
        if keypress == curses.KEY_RIGHT:
            current_frame = min(board['num_frames'] - 1, current_frame + 1)


if __name__ == '__main__':
    try:
        # Initialize curses
        stdscr = curses.initscr()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
        main(stdscr)                    # Enter the main loop
        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()                 # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception
