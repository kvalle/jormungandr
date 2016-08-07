#!/usr/bin/env python3
# encoding: utf-8

import sys
import time
import curses

ROWS = 10
COLS = 32

content = [0] * ROWS
content[3] = 31

def to_bits(v):
    return [(v >> i) & 1 for i in reversed(range(COLS))]

def from_bits(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

def draw_frame(win):
    def row_to_str(row):
        bits = to_bits(content[row])
        #map(str, bits)
        bits = map(lambda b: "\u2588" if b==1 else " ", bits)
        return "".join(bits)

    for row in range(ROWS):
        win.addstr(row, 0, row_to_str(row))

def draw_background(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 0, "+————————————————————————————————")
    for i in range(0, ROWS):
        stdscr.addstr(2 + i, 0, "|")
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(False)
    draw_background(stdscr)

    win = curses.newwin(ROWS, COLS + 1, 2, 1)

    for i in range(10):
        content[3] = content[3] << 1
        draw_frame(win)
        win.refresh()
        win.getkey()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
