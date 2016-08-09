#!/usr/bin/env python3
# encoding: utf-8

import sys
import time
import curses

import bits

ROWS = 20
COLS = 80

class GameState:
    snake = [0] * ROWS
    head = { "row": 0, "col": 0 }
    tail = { "row": 0, "col": 0 }
    stack = []
    running = True
    score = 0
    direction = "right"

    def __init__(self, start_length=30):
        self.snake[0] = bits.first_n_set(start_length, length=COLS)
        self.head["col"] = start_length
        self.stack = ["right"] * start_length
        self.direction = "right"

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

def set_cell(pos, state):
    state.snake[pos["row"]] = state.snake[pos["row"]] | 1 << (COLS - pos["col"])

def unset_cell(pos, state):
    state.snake[pos["row"]] = state.snake[pos["row"]] & ~(1 << (COLS - pos["col"]))
    
def move_snake_head(state):
    state.stack.append(state.direction)
    state.head = move(state.head, state.direction)
    set_cell(state.head, state)
 
def move_snake_tail(state):
    unset_cell(state.tail, state)
    state.tail = move(state.tail, state.stack.pop(0))

def debug(stdscr, text):
    stdscr.addstr(ROWS + 5, 0, text)
    stdscr.refresh()

def get_direction(key, state):
    if state.stack[-1] != "right" and key == curses.KEY_LEFT:
        return "left"
    if state.stack[-1] != "left" and key == curses.KEY_RIGHT:
        return "right"
    if state.stack[-1] != "up" and key == curses.KEY_DOWN:
        return "down"
    if state.stack[-1] != "down" and key == curses.KEY_UP:
        return "up"
    else:
        return state.direction

def detect_collision(state):
    next_head = move(state.head, state.direction)

    wall_collision = next_head["row"] < 0 or \
       next_head["row"] >= ROWS or \
       next_head["col"] <= 0 or \
       next_head["col"] > COLS
    
    tail_collision = state.snake[next_head["row"]] & (1 << (COLS - next_head["col"]))

    if wall_collision or tail_collision:
        state.running = False

class GameInputs():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        stdscr.nodelay(True)

    def get_direction(self, state):
        key = self.stdscr.getch()

        if state.stack[-1] != "right" and key == curses.KEY_LEFT:
            return "left"
        if state.stack[-1] != "left" and key == curses.KEY_RIGHT:
            return "right"
        if state.stack[-1] != "up" and key == curses.KEY_DOWN:
            return "down"
        if state.stack[-1] != "down" and key == curses.KEY_UP:
            return "up"
        else:
            return state.direction

class GameWindow():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.curs_set(False)

        self.win = curses.newwin(ROWS + 2, COLS + 2, 1, 0)
        self.win.border()

    def update_title(self, state):
        self.stdscr.addstr(0, 0, " jormungandr <> score: " + str(state.score))
        if not state.running:
            self.stdscr.addstr(0, COLS - 8, "GAME OVER", curses.A_BLINK)
        self.stdscr.refresh()

    def draw_frame(self, state):
        def row_to_str(row):
            bs = bits.to_bitlist(row, length=COLS)
            bs = map(lambda b: "o" if b==1 else " ", bs)
            return "".join(bs)

        self.win.border()
        
        for row in range(ROWS):
            style = curses.color_pair(2) if state.running else curses.A_NORMAL
            self.win.addstr(row+1, 1, row_to_str(state.snake[row]), style)

        self.win.refresh()


def main(stdscr):
    state = GameState()
    window = GameWindow(stdscr)
    inputs = GameInputs(stdscr)

    window.update_title(state)
    
    while True:
        # wait for next frame
        time.sleep(0.1)

        # inputs
        state.direction = inputs.get_direction(state)

        # update game
        detect_collision(state)
        if state.running:
            state.score += 1
            move_snake_head(state)
            move_snake_tail(state)
        
        # outputs
        window.update_title(state)
        window.draw_frame(state)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
