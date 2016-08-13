#!/usr/bin/env python3
# encoding: utf-8

import time
import curses

ROWS = 20
COLS = 80
DEBUG = False

class GameState:
    snake = None
    head = {"row": 0, "col": 0}
    tail = {"row": 0, "col": 0}
    stack = []
    running = True
    score = 0
    direction = "right"

    def __init__(self, start_length=30):
        self.snake = [[row == 0 and col <= start_length
            for col in range(COLS)]
            for row in range(ROWS)]
        self.head["col"] = start_length
        self.stack = ["right"] * start_length
        self.direction = "right"

    def detect_collision(self):
        next_head = moved(self.head, self.direction)

        def wall_collision():
            return next_head["row"] < 0 or \
                next_head["row"] >= ROWS or \
                next_head["col"] <= 0 or \
                next_head["col"] > COLS
        
        def tail_collision():
            return self.snake[next_head["row"]][next_head["col"]]

        if wall_collision() or tail_collision():
            self.running = False

    def move_snake_head(self):
        self.stack.append(self.direction)
        self.head = moved(self.head, self.direction)
        self.set_cell(self.head)
     
    def move_snake_tail(self):
        self.unset_cell(self.tail)
        self.tail = moved(self.tail, self.stack.pop(0))

    def set_cell(self, pos):
        self.snake[pos["row"]][pos["col"]] = True

    def unset_cell(self, pos):
        self.snake[pos["row"]][pos["col"]] = False


def moved(pos, direction):
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
        raise Exception("bad direction: " + direction)

    return pos

def debug(text):
    global DEBUG
    if DEBUG != False:
        DEBUG += text

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
        self.win.border()
        
        for row in range(ROWS):
            style = curses.color_pair(2) if state.running else curses.A_NORMAL
            row_string = "".join(map(lambda b: "\u25CF" if b else " ", state.snake[row]))
            self.win.addstr(row + 1, 1, row_string, style)

        self.win.refresh()

    def draw_debug(self):
        global DEBUG

        if not DEBUG:
            return

        i = 0
        while DEBUG:
            line = DEBUG[:COLS]
            DEBUG = DEBUG[COLS:]
            self.stdscr.addstr(ROWS + 5 + i, 0, line)
            i += 1

        self.stdscr.refresh()


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
        state.detect_collision()
        if state.running:
            state.score += 1
            state.move_snake_head()
            state.move_snake_tail()
        
        # outputs
        window.update_title(state)
        window.draw_frame(state)
        window.draw_debug()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
