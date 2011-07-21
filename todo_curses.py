#!/usr/bin/python

import os
import re
import locale
import string
import curses
from sqlite_db import SQLite

DATABASE_PATH = os.path.normpath(os.path.join(
    os.path.expanduser("~"),"todo.db")) 
_db = None
TEMPDISPLAY = None
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

def add(lst):
    """ Add a new entry to the database.
        Preconditions:
            List of lists containing (key,val) pair."""
    
    global _db
    global TEMPDISPLAY

    entry    = ""
    due      = ""
    priority = ""
    for i in lst:
        if i[0] == "entry":
            entry = i[1]
            entry = entry.lstrip('"')
            entry = entry.rstrip('"')
        elif i[0] == "due":
            due = i[1]
            due = due.lstrip('"')
            due = due.rstrip('"')
        elif i[0] == "priority":
            priority = i[1]

    printwin(TEMPDISPLAY,10,10,entry)
    return #_db.add(due, entry, priority)

def get(lst):
    """ Get all entries that fit user criteria.
        Preconditions:
            List of lists containing (key,val) pair
        Postconditions:
            Returns string"""
    
    global _db

    statement = _db.get_prepare(lst)
    data = _db.get(statement)
    output = ""
    for i in data:
        for j in i:
            output += str(j) + "\t"
        output += "\n"
    
    return output

def parse(inpt):
    """ Parse input string.
        Preconditions:
            inpt - User input
        Postconditions:
            -1 : quit
             0 : help
             1 : get
             2 : add
             3 : delete
             List of key/value lists"""

    inpt_list = inpt.strip().split()
    
    cmd = inpt_list.pop(0).lower()
    if cmd == "quit":
        return -1,[]
    elif cmd == "get":
        lst = []
        for i in inpt_list:
            keyvalpair = i.split("=")
            lst.append(keyvalpair)

        return 1,get(lst)
    elif cmd == "add":
        lst = []
        for i in inpt_list:
            keyvalpair = i.split("=")
            lst.append(keyvalpair)
        
        return 2,add(lst)
    elif cmd == "delete":
        return 3,[]
    elif cmd == "help":
        return 0, [] 

    return 0,[]


def main():
    global TEMPDISPLAY
    global _db
    # Set up
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    _db = SQLite()
    
    if not (os.path.isfile(DATABASE_PATH)):
        _db.create(DATABASE_PATH)
    else:
        _db.open(DATABASE_PATH)

    screen  = curses.initscr()
    y,x = screen.getmaxyx()
    
    display = create_window(y-2,x,0,0)
    prompt  = create_window(2,x,y-2,0)
    TEMPDISPLAY = display # delete
    printwin(prompt, 0,0, "> ")
    #End setup.

    inpt      = prompt.getstr()
    val,data  = parse(inpt)
    while val != -1:
        if val == 0:
            printwin(display,0,0,"Invalid")
        elif val == 1:
            printwin(display,0,0, data)

        clearwin(display, 0, 0)
        clearwin(prompt, 2, 0)
        inpt = prompt.getstr(0,2)
        val,data  = parse(inpt)

    # Clean up.
    destroy_window(display)
    destroy_window(prompt)

    curses.endwin()
    _db.close()


if __name__ == '__main__':
    main()
