import os
import sys
import time
import random
import select
import termios
import tty
import shutil


# ANSI escape color codes
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Game objects
HEAD = BLUE + "@"
BODY = GREEN + "O"
SNACK = GREEN + "$"

# NOTE: Always use width = width + 1 when referencing width
# due to the addition of '\n' character


def init_arena(height, width):
    screen = []
    red_border = "\x1b[31m#"
    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1:
                screen.append(red_border)
            elif j == 0 or j == width - 1:
                screen.append(red_border)
            else:
                screen.append(" ")

        screen.append("\n")
    # initialize snake and snack
    snake = Snake(width, height)
    snack = Snack(snake, width, height)
    draw_snake_in_arena(screen, snake, width)
    draw_random_snack(screen, width, snack)
    return screen, snake, snack


class Snack:
    # initialize to random positon on the screen
    def __init__(self, snake, width, height):
        self.randomize_pos(snake, width, height)

    def randomize_pos(self, snake, width, height):
        rand_x, rand_y = snake.posx, snake.posy
        while rand_x == snake.posx or rand_y == snake.posy:
            rand_x = random.randint(1, width - 1)
            rand_y = random.randint(1, height - 1)
        self.posx, self.posy = rand_x, rand_y


def update_arena(screen, snake, snack):
    index = get_index(width, snake)
    # only spawn snack if not taken
    if screen[index] == "$":
        snack.randomize_pos(snake, width, height)
        draw_random_snack(screen, width, snack)
    draw_snake_in_arena(screen, snake, width)


def get_index(width, obj):
    return obj.posy * width + 1 + obj.posx


def draw_snake_in_arena(screen, snake, width):
    index = get_index(width, snake)
    screen[index] = HEAD
    for i in range(1, 4):
        screen[index - i] = BODY


def draw_random_snack(screen, width, snack):
    index = get_index(width, snack)
    screen[index] = SNACK


class Snake:
    def __init__(self, posx, posy):
        self.posx = posx - 2
        self.posy = posy - 2
        self.direction_x = 0
        self.direction_y = 0

    def move(self, x, y):
        self.direction_x = x
        self.direction_y = y

    def update(self, arena, width):
        # block update if it will collide with snake body
        ch = arena[get_index(width, self)]
        if ch != BODY:
            self.posx += self.direction_x
            self.posy += self.direction_y


# non blocking input
def get_key_input():
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    return None


def setup_terminal():
    """Configure terminal for game input (no echo, raw mode)"""
    old_settings = termios.tcgetattr(sys.stdin)
    # Disable echo and canonical mode
    new_settings = old_settings[:]
    new_settings[3] &= ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)
    return old_settings


def restore_terminal(old_settings):
    """Restore original terminal settings"""
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    size = shutil.get_terminal_size()
    # print(f"width: {size.columns}, height: {size.lines}")
    width, height = size.columns // 2, size.lines // 2

    escape_keys = ["q", "\x1b", "\x03"]
    arena, snake, snack = init_arena(height, width)
    old_settings = setup_terminal()
    sys.stdout.write("\033[2J\033[H")
    # draw starting position
    sys.stdout.write("".join(arena))
    # game loop
    while True:
        ch = get_key_input()
        lower_ch = ch.lower() if ch is not None else ""

        match lower_ch:
            case lower_ch if lower_ch in escape_keys:
                break
            case "w":
                snake.move(0, -1)
            case "s":
                snake.move(0, 1)
            case "a":
                snake.move(-1, 0)
            case "d":
                snake.move(1, 0)
        # update snakes movement
        snake.update(arena, width)

        # check if snake within arena
        if (
            snake.posx >= width - 1
            or snake.posx <= 0
            or snake.posy >= height - 1
            or snake.posy <= 0
        ):
            break
        update_arena(arena, snake, snack)
        # clear arena
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write("".join(arena))
        time.sleep(0.15)
    restore_terminal(old_settings)
