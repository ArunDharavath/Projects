#importing all necessary libraries
import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Do you want to measure your typing speed?")
    stdscr.addstr("\nHit any key to start!")
    stdscr.refresh()
    stdscr.getkey()

#fn that displays the text to be typed and allows typing by user
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(5, 0, f"WPM: {wpm}")

    #takes each character typed by user and compares against actual text
    #to display correct input in green, wrong input in red and yellow highlight
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

#fn to randomly display typing text
def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

#wrapper function for display_text()
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)

        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        #ESC key to quit the app
        if ord(key) == 27:
            break
        
        #delete previous char for user
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        else:
            current_text.append(key)   
    return wpm 

#main fn that calls the other functions to run the app
def main(stdscr):
    #pairing of foreground and background
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    
    start_screen(stdscr)

    #loop to ask user if they want to continue or stop
    while True:
        words = wpm_test(stdscr)
        stdscr.addstr(2, 0, f"You have finished the test with {words} WORDS PER MINUTE! Press any key to play again.")
        key = stdscr.getkey()
        
        #ESC key to quit the program
        if ord(key) == 27:
            break

#initialises the curses module and allows to perform different functions on the terminal
wrapper(main)