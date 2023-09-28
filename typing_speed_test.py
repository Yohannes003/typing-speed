import curses
import time
import random
from curses import wrapper


def screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "\nwelcome to the  typing speed test")
    stdscr.addstr("\n press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def user_text_input(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"wpm: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def given_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def speed(stdscr):
    displayed_text = given_text()
    written_text = []
    wpm = 0
    starting_time = time.time()
    stdscr.nodelay(True)

    while True:
        passed_time = max(time.time() - starting_time, 1)
        wpm = round(len(written_text) / (passed_time / 60) / 5)

        stdscr.clear()
        user_text_input(stdscr, displayed_text, written_text, wpm)
        stdscr.refresh()

        if "".join(written_text) == displayed_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(written_text) > 0:
                written_text.pop()
        elif len(written_text) < len(displayed_text):
            written_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

    screen(stdscr)
    while True:
        speed(stdscr)

        stdscr.addstr(2, 0, " test completed, press any key to continue")
        stdscr.getkey()
        stdscr.clear()


wrapper(main)
