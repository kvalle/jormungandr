#!/usr/bin/env python3
# encoding: utf-8

import sys
import time
import curses

ROWS = 10
COLS = 32

snake = [0] * ROWS

snake[4] = 7 << (COLS - 3)
head = { "row": 4, "col": 3 }
tail = { "row": 4, "col": 0 }
direction = "left"

def move_head(row, col):
    snake[row] = snake[row] | 1 << (COLS - col)
    head["col"] = col

def remove_tail(row, col):
    snake[row] = snake[row] & ~(1 << (COLS - col))
    tail["col"] += 1 # naive

def move_snake():
    if direction == "left":
        move_head(head["row"], head["col"] + 1)
        remove_tail(tail["row"], tail["col"])

    elif direction == "right":
        pass

def to_bits(v):
    return [(v >> i) & 1 for i in reversed(range(COLS))]

def from_bits(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

def draw_frame(win):
    def row_to_str(row):
        bits = to_bits(snake[row])
        bits = map(lambda b: "o" if b==1 else " ", bits)
        return "".join(bits)

    win.border()
    
    for row in range(ROWS):
        win.addstr(row+1, 1, row_to_str(row))


def main(stdscr):
    curses.curs_set(False)
    stdscr.addstr(0, 0, " score: 0")
    stdscr.refresh()
    
    win = curses.newwin(ROWS + 2, COLS + 2, 1, 0)
    win.border()

    for i in range(10):
        move_snake()
        draw_frame(win)
        win.refresh()
        win.getkey()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
