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
stack = ["left", "left", "left"]

def move(pos, direction):
    if direction == "up":
        pos["row"] -= 1
    elif direction == "down":
        pos["row"] += 1
    elif direction == "left":
        pos["col"] -= 1
    elif direction == "right":
        pos["col"] += 1
    else:
        raise Exception("wrong direction: " + direction)

    return pos   

def set_cell(pos):
    snake[pos["row"]] = snake[pos["row"]] | 1 << (COLS - pos["col"])

def unset_cell(pos):
    snake[pos["row"]] = snake[pos["row"]] | 1 << (COLS - pos["col"])


def remove_tail(row, col):
    snake[row] = snake[row] & ~(1 << (COLS - col))
    
    direction = stack[0]
    if direction == "right":
        tail["row"] = tail["row"]
        tail["col"] = tail["col"] + 1       
    elif direction == "left":
        tail["row"] = tail["row"]
        tail["col"] = tail["col"] - 1
    elif direction == "up":
        tail["row"] = tail["row"] - 1
        tail["col"] = tail["col"]
    elif direction == "down":
        tail["row"] = tail["row"] + 1
        tail["col"] = tail["col"]

def move_snake(direction):
    global head

    if direction == "right":
        head = move(head, "right")
        
    elif direction == "left":
        head = move(head, "left")

    elif direction == "up":
        head = move(head, "up")

    elif direction == "down":
        head = move(head, "down")

    set_cell(head)

    stack.append(direction)
    stack.pop(0)

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

def debug(stdscr, text):
    stdscr.addstr(ROWS + 5, 0, text)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(False)
    stdscr.addstr(0, 0, " score: 0")
    stdscr.refresh()
    
    win = curses.newwin(ROWS + 2, COLS + 2, 1, 0)
    win.border()
    win.nodelay(True)

    while True:
        key = win.getch()
        if key == ord('a'):
            move_snake("left")
        if key == ord('d'):
            move_snake("right")
        if key == ord('s'):
            move_snake("down")
        if key == ord('w'):
            move_snake("up")

        draw_frame(win)
        win.refresh()
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
