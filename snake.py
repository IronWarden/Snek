import os
import sys
import time
import random
import select
import termios
import tty
import shutil


BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


def draw_arena(height, width):
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

    return screen


def draw_snake_in_arena(screen, snake, width):
    index = snake.posy * width + snake.posx
    screen[index] = BLUE + "@"
    for i in range(1, 4):
        screen[index - i] = GREEN + "O"

def draw_random_snack(screen, width, height, snake):
    rand_x, rand_y = 0, 0
    while rand_x == snake.posx or rand_y == snake.posy:
        rand_x = random.randint(0, width * height - 1)
        rand_y = random.randint(0, width * height - 1)
    index =  

class Snake:
    def __init__(self, posx=18, posy=4):
        self.posx = posx
        self.posy = posy

    def move(self, x, y):
        self.posx += x
        self.posy += y


if __name__ == "__main__":
    size = shutil.get_terminal_size()
    # print(f"width: {size.columns}, height: {size.lines}")
    width, height = size.columns, size.lines

    escape_keys = ["q", "\x1b", "\x03"]
    arena = draw_arena(height // 2, width // 2)
    snake = Snake()
    draw_snake_in_arena(arena, snake, width // 2)
    sys.stdout.write("".join(arena))

    # game loop
    while True:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch.lower() in escape_keys:
            break
