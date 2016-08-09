#!/usr/bin/env python3
# encoding: utf-8

import sys
import time
import curses

ROWS = 20
COLS = 80

snake = [0] * ROWS

snake[4] = 7 << (COLS - 3)
head = { "row": 4, "col": 3 }
tail = { "row": 4, "col": 0 }
stack = ["right", "right", "right"]

running = True

score = 0

def move(pos, direction):
    pos = pos.copy()

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
        win.addstr(row+1, 1, row_to_str(row), curses.color_pair(2))

def debug(stdscr, text):
    stdscr.addstr(ROWS + 5, 0, text)
    stdscr.refresh()

def get_direction(key, direction):
    if stack[-1] != "right" and key == curses.KEY_LEFT:
        return "left"
    if stack[-1] != "left" and key == curses.KEY_RIGHT:
        return "right"
    if stack[-1] != "up" and key == curses.KEY_DOWN:
        return "down"
    if stack[-1] != "down" and key == curses.KEY_UP:
        return "up"
    else:
        return direction

def collision_detected(direction):
    next_head = move(head, direction)
    return next_head["row"] < 0 or \
       next_head["row"] >= ROWS or \
       next_head["col"] <= 0 or \
       next_head["col"] > COLS

def update_title(stdscr, score, running=True):
    stdscr.addstr(0, 0, " jormungandr <> score: " + str(score))
    if not running:
        stdscr.addstr(0, COLS - 8, "GAME OVER", curses.A_BLINK)
    stdscr.refresh()

def main(stdscr):
    global score, running

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(False)
    stdscr.nodelay(True)
    update_title(stdscr, score=score, running=True)
    
    win = curses.newwin(ROWS + 2, COLS + 2, 1, 0)
    win.border()

    direction = "right"
    while True:
        # wait for next frame
        time.sleep(0.1)

        if running:
            # inputs
            direction = get_direction(stdscr.getch(), direction)
            
            # update game
            score += 1
            if collision_detected(direction):
                running = False
                continue
            move_snake_head(direction)
            move_snake_tail()
            
            # outputs
            update_title(stdscr, score=score)
            draw_frame(win)
            win.refresh()
            
        else:
            update_title(stdscr, score=score, running=False)

        

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
