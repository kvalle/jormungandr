#!/usr/bin/env python3
# encoding: utf-8

import sys
import random
import time
import curses
from enum import Enum

ROWS = 20
COLS = 80

class Action(Enum):
    up = 1
    down = 2
    left = 3
    right = 4
    new = 5
    quit = 6

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def moved(self, direction):
        if direction == Action.up:
            return Position(self.row - 1, self.col)
        elif direction == Action.down:
            return Position(self.row + 1, self.col)
        elif direction == Action.left:
            return Position(self.row, self.col - 1)
        elif direction == Action.right:
            return Position(self.row, self.col + 1)
        else:
            raise Exception("bad direction: " + direction)

class GameState:
    def __init__(self, start_length=5):
        self.snake = [[False for col in range(COLS)] for row in range(ROWS)]
        self.head = Position(0, 0)
        self.tail = Position(0, 0)
        self.food = None
        self.stack = []
        self.running = True
        self.score = 0
        self.direction = Action.right

        random.seed()
        self.move_food()
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
                next_head.col < 0 or \
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


class GameInputs():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        stdscr.nodelay(True)

    def get_action(self, state):
        key = self.stdscr.getch()

        if state.stack[-1] != Action.right and key == curses.KEY_LEFT:
            return Action.left
        if state.stack[-1] != Action.left and key == curses.KEY_RIGHT:
            return Action.right
        if state.stack[-1] != Action.up and key == curses.KEY_DOWN:
            return Action.down
        if state.stack[-1] != Action.down and key == curses.KEY_UP:
            return Action.up
        if key == ord('q'):
            return Action.quit
        if key == ord('n'):
            return Action.new
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

    def draw(self, state):
        self.stdscr.clear()

        self.draw_title(state)
        self.draw_frame(state)

    def draw_title(self, state):
        self.stdscr.addstr(0, 0, " jormungandr <> score: " + str(state.score))
        if not state.running:
            self.stdscr.addstr(0, COLS - 8, "GAME OVER", curses.A_BLINK)
        self.stdscr.addstr(ROWS + 3, 0, " press Q to quit, N to start new game")
        self.stdscr.refresh()

    def draw_frame(self, state):
        self.win.border()
        
        green = curses.color_pair(2) if state.running else curses.A_NORMAL
        for row in range(ROWS):
            row_string = "".join(map(lambda b: "\u25CF" if b else " ", state.snake[row]))
            self.win.addstr(row + 1, 1, row_string, green)

        red = curses.color_pair(1) if state.running else curses.A_NORMAL
        self.win.addstr(state.food.row + 1, state.food.col + 1, "x", red)        

        self.win.refresh()


def main(stdscr):
    state = GameState()
    window = GameWindow(stdscr)
    inputs = GameInputs(stdscr)

    while True:
        time.sleep(0.1)
        
        action = inputs.get_action(state)
        if action == Action.quit:
            sys.exit(0)
        elif action == Action.new:
            state = GameState()
            continue
        else:
            state.direction = action

        state.update()
        window.draw(state)

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
