import os
import sys
import time
import random
import select
import termios
import tty
import shutil


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


if __name__ == "__main__":
    size = shutil.get_terminal_size()
    # print(f"width: {size.columns}, height: {size.lines}")
    width, height = size.columns, size.lines

    escape_keys = ["q", "\x1b", "\x03"]
    arena = draw_arena(height // 2, width // 2)

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
