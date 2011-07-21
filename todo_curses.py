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
TEMPDISPLAY = None # TODO: Delete
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
    """ Print to specified window coordinates.
        Preconditions:
            window - curses's window to print to.
                 x - x-coord
                 y - y-coord
              data - String to be printed to screen
        Postconditions:
            String is added to window, and window is refreshed."""
    
    window.addstr(y,x,data)
    window.refresh()

def clearwin(window, startx, starty):
    """ Clear the specified window starting at specified (x,y) 
        Preconditions:
            window - Window to be cleared.
            startx - x-coord to start at.
            starty - y-coord to start at."""

    y,x = window.getmaxyx()

    for i in range(startx, x-1):
        for j in range(starty, y-1):
            window.addstr(j,i," ")

def printhelp():
    """ Return help string """
    strng  = "add entry=\"<entry>\" due=\"<due>\" priority=\"<priority>\""
    strng +=" \nview [all] [[priority=<priority>] [due=<due>] [start=<start>]"
    strng += "[completed=<completed>]]"
    strng += "\ndelete [all] [id=\"<id>\"] [[due=\"<due>\"]"
    strng += "[priority=\"<priority>\" completed=\"<T/F>\"]]"

    return strng

def stripquotes(strng):
    return strng.lstrip('"').rstrip('"')

def add(lst):
    """ Add a new entry to the database.
        Preconditions:
            List of lists containing (key,val) pair."""
    
    global _db
    entry    = ""
    due      = ""
    priority = ""
    for i in lst:
        if i[0] == "entry":
            entry = stripquotes(i[1])
        elif i[0] == "due":
            due = stripquotes(i[1])
        elif i[0] == "priority":
            priority = stripquotes(i[1]) 

    return _db.add(due, entry, priority)

def delete(lst):
    """ Delete an entry from the database.
        Preconditions:
            List of lists containing (key,val) pair.
        Postconditions:
            True if successful, else False"""
    
    global _db

    if len(lst) == 0:
        return False

    if len(lst) == 1 and lst[0][0] == "all":
        return _db.purge() 
    
    # First check if id was supplied
    for i in lst:
        if i[0] == "id":
            ident = int(i[1])
            break

    if ident == -1:
        statement = _db.get_prepare(lst)
        rws       = _db.get(statement)
        ident     = rws[0][0]
    
    return _db.delete(ident)
    

def view(lst):
    """ Get all entries that fit user criteria.
        Preconditions:
            List of lists containing (key,val) pair
        Postconditions:
            Returns string"""
    
    global _db

    statement = _db.get_prepare(lst)
    data = _db.get(statement)
    output = ""
    # TODO: Rewrite
    for i in data:
        for j in i:
            output += str(j) + " | "
        output += "\n"
    
    return output

def parse(inpt):
    """ Parse input string.
        Preconditions:
            inpt - User input
        Postconditions:
            -1 : quit
             0 : help
             1 : view
             2 : add
             3 : delete
             4 : edit
             List of key/value lists"""
    inpt_list = inpt.strip().split()
    
    cmd = inpt_list.pop(0).lower()
    if cmd == "quit":
        return -1,[]
    elif cmd == "view":
        lst = []
        for i in inpt_list:
            keyvalpair = i.split("=")
            lst.append(keyvalpair)
    
        if len(lst) == 0:
            lst.append(["all"])

        return 1,view(lst)
    elif cmd == "add":
        lst = re.findall(' (.*?)="(.*?)"', inpt)
        # TODO: Check for no values
        return 2,add(lst)
    elif cmd == "delete":
        lst = []
        if len(inpt_list) == 1 and inpt_list[0].lower() == "all":
            lst.append(["all"])
        else:
            reg = re.findall(' (.*?)="(.*?)"', inpt)
            for i in reg:
                arr = [i[0], i[1]]
                lst.append(arr)
        
        return 3,delete(lst)
    elif cmd == "edit":
        return 4,[]
    elif cmd == "help":
        return 0, printhelp()

    return 0,[]


def main():
    global TEMPDISPLAY # TODO: delete
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
    TEMPDISPLAY = display # TODO: delete
    printwin(prompt, 0,0, "> ")
    #End setup.

    inpt      = prompt.getstr()
    val,data  = parse(inpt)
    while val != -1:
        if val == 0 or val == 1:
            printwin(display,0,0,data)
        elif val > 1:
            printwin(display,0,0,view([["all"]]))

        clearwin(display, 0, 0)
        clearwin(prompt, 2, 0)
        inpt = prompt.getstr(0,2)
        val,data  = parse(inpt)

    # Clean up.
    destroy_window(display)
    destroy_window(prompt)

    #restorescreen()
    _db.close()

def restorescreen():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    main()
    #try:
    #    main()
    #except:
    #    restorescreen()
