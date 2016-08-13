#!/usr/bin/env python3
# encoding: utf-8

import random
import time
import curses

ROWS = 20
COLS = 80
DEBUG = False

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def moved(self, direction):
        if direction == "up":
            return Position(self.row - 1, self.col)
        elif direction == "down":
            return Position(self.row + 1, self.col)
        elif direction == "left":
            return Position(self.row, self.col - 1)
        elif direction == "right":
            return Position(self.row, self.col + 1)
        else:
            raise Exception("bad direction: " + direction)

class GameState:
    snake = [[False for col in range(COLS)] for row in range(ROWS)]
    head = Position(0, 0)
    tail = Position(0, 0)
    food = Position(15, 15)
    stack = []
    running = True
    score = 0
    direction = "right"

    def __init__(self, start_length=5):
        random.seed()
        for _ in range(start_length - 1):
            self.move_snake_head()

    def update(self):
        if self.detect_collision():
            self.running = False

        if not self.running:
            return

        if self.detect_eating():
            self.score += 1
            self.move_food()
        else:
            self.move_snake_tail()

        self.move_snake_head()

    def detect_collision(self):
        next_head = self.head.moved(self.direction)

        def wall_collision():
            return next_head.row < 0 or \
                next_head.row >= ROWS or \
                next_head.col <= 0 or \
                next_head.col >= COLS
        
        def tail_collision():
            return self.snake[next_head.row][next_head.col]

        return wall_collision() or tail_collision()

    def detect_eating(self):
        next_head = self.head.moved(self.direction)
        return self.food == next_head

    def move_snake_head(self):
        self.stack.append(self.direction)
        self.head = self.head.moved(self.direction)
        self.snake[self.head.row][self.head.col] = True
     
    def move_snake_tail(self):
        self.snake[self.tail.row][self.tail.col] = False
        self.tail = self.tail.moved(self.stack.pop(0))

    def move_food(self):
        free = len([cell for row in self.snake for cell in row if not cell])
        num = random.randrange(0, free)

        for row in range(ROWS):
            for col in range(COLS):
                if not self.snake[row][col]:
                    num -= 1
                if num == 0:
                    self.food = Position(row, col)
                    return

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
        
        style = curses.color_pair(2) if state.running else curses.A_NORMAL
        for row in range(ROWS):
            row_string = "".join(map(lambda b: "\u25CF" if b else " ", state.snake[row]))
            self.win.addstr(row + 1, 1, row_string, style)

        style = curses.color_pair(1) if state.running else curses.A_NORMAL
        self.win.addstr(state.food.row + 1, state.food.col + 1, "x", style)        

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
        state.update()
        
        # outputs
        window.update_title(state)
        window.draw_frame(state)
        window.draw_debug()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
