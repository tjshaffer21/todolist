#!/usr/bin/python

import os
import locale
import string
import curses
from sqlite_db import SQLite

DATABASE_PATH = os.path.normpath(os.path.join(
    os.path.expanduser("~"),"todo.db")) 

def create_window(height, width, starty, startx):
    """ Create a new window.
        Preconditions:
            height - height of the window
            width  - width of the window
            starty - starting y position
            startx - starting x position
        Postconditions:
            Create a new window and refresh the window.
            Returns the window."""
    
    window = curses.newwin(height, width, starty, startx)
    window.refresh()

    return window

def destroy_window(window):
    """ Clear window and destroy it.
        Preconditions:
            window - window to be destroyed."""
    
    y,x = window.getmaxyx()

    for i in range(x-1):
        for j in range(y-1):
            window.addstr(j,i,' ')

    window.refresh()

    del window

def printwin(window, x, y, data):
    """ Print to specified window coordinates. """
    window.addstr(y,x,data)
    window.refresh()

def clearwin(window, startx, starty):
    """ Clear the specified window starting at specified (x,y) """
    y,x = window.getmaxyx()

    for i in range(startx, x-1):
        for j in range(starty, y-1):
            window.addstr(j,i," ")

def parse(inpt):
    """ Parse input string. """
    inpt = inpt.strip()

    if inpt == "quit":
        return -1

    return 0


def main():
    # Set up
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    db = SQLite()
    
    if not (os.path.isfile(DATABASE_PATH)):
        db.create(DATABASE_PATH)
    else:
        db.open(DATABASE_PATH)

    screen  = curses.initscr()
    y,x = screen.getmaxyx()
    
    display = create_window(y-2,x,0,0)
    prompt  = create_window(2,x,y-2,0)

    printwin(prompt, 0,0, "> ")
    #End setup.

    inpt = prompt.getstr()
    val  = parse(inpt)
    while val != -1:
        printwin(display, 0, 0, inpt)
        
        clearwin(prompt, 2, 0)
        inpt = prompt.getstr(0,2)
        val  = parse(inpt)

    # Clean up.
    destroy_window(display)
    destroy_window(prompt)

    curses.endwin()
    db.close()


if __name__ == '__main__':
    main()
