#!/usr/bin/env python3
# encoding: utf-8

import sys
import time
import curses

ROWS = 50
COLS = 80

snake = [0] * ROWS

snake[4] = 7 << (COLS - 3)
head = { "row": 4, "col": 3 }
tail = { "row": 4, "col": 0 }
stack = ["right", "right", "right"]

running = True

score = 0

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
    snake[pos["row"]] = snake[pos["row"]] & ~(1 << (COLS - pos["col"]))
    
def move_snake_head(direction):
    global head
    stack.append(direction)
    head = move(head, direction)
    set_cell(head)
    
def move_snake_tail():
    global tail
    unset_cell(tail)
    tail = move(tail, stack.pop(0))

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

def get_direction(key, direction):
    if stack[-1] != "right" and key == ord('a'):
        return "left"
    if stack[-1] != "left" and key == ord('d'):
        return "right"
    if stack[-1] != "up" and key == ord('s'):
        return "down"
    if stack[-1] != "down" and key == ord('w'):
        return "up"
    else:
        return direction

def collision_detected():
    return head["row"] < 0 or \
       head["row"] >= ROWS or \
       head["col"] < 0 or \
       head["col"] >= COLS

def update_title(stdscr, score, running=True):
    stdscr.addstr(0, 0, " score: " + str(score))
    if not running:
        stdscr.addstr(0, COLS - 8, "GAME OVER")
    stdscr.refresh()

def main(stdscr):
    global score, running

    curses.curs_set(False)
    update_title(stdscr, score=score, running=True)
    
    win = curses.newwin(ROWS + 2, COLS + 2, 1, 0)
    win.border()
    win.nodelay(True)

    direction = "right"
    while True:
        # wait for next frame
        time.sleep(0.1)

        if not running:
            update_title(stdscr, score=score, running=False)
            continue

        # inputs
        direction = get_direction(win.getch(), direction)
        
        # update game
        score += 1
        move_snake_head(direction)
        if collision_detected():
            running = False
            continue
        move_snake_tail()
        #debug(stdscr, str(tail) + "    score = " + str(score) + "                                ")
        
        # outputs
        update_title(stdscr, score=score)
        draw_frame(win)
        win.refresh()

        


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
