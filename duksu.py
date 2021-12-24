#!/usr/bin/python3
import curses, random
# import sys, tty
from curses import wrapper

screen = curses.initscr()
maxY, maxX = screen.getmaxyx()
curses.curs_set(0)

DIRECTION = ["RIGHT", "LEFT", "UP", "DOWN"]

class win:
    pass

class Pet:
    maxY, maxX = screen.getmaxyx()
    def __init__(self, name, direction = "RIGHT", posY = 1, posX = 1):
        self.name = name
        self.direction = direction
        self.posY = posY
        self.posX = posX
        self.icon = "d"

    def facing(self):
        if self.direction == "RIGHT" or self.direction == "UP":
            self.icon = "D"
        else:
            self.icon = "ᗡ"

    def waddle(self):
        if self.posX < maxX/2 - 2 and self.direction == "RIGHT":
            self.posX += 1
            return self.posY, self.posX
        elif self.posX > 1 and self.direction == "LEFT":
            self.posX -= 1
            return self.posY, self.posX
        elif self.posY > 1 and self.direction == "UP":
            self.posY -= 1
            return self.posY, self.posX
        elif self.posY < maxY/2 - 2 and self.direction == "DOWN":
            self.posY += 1
            return self.posY, self.posX

    def placeIcon(self):
        return self.posY, self.posX, self.icon

class MenuWindow:
    def __init__(self, title, h, w, y, x):
        self.window = curses.newwin(h, w, y, x)
        self.window.nodelay(True)
        self.window.box()
        self.window.addstr(1,2, title)
        self.window.refresh()

    def refresh(self):
        self.window.refresh()

    def clear(self):
        for y in range(3, self.window.getmaxyx()[0]-1):
            self.window.move(y,2)
            self.window.clrtoeol()
        self.window.box()

    def addstr(self, y, x, string, attr=0):
        self.window.addstr(y, x, string, attr)

    # Resize windows when terminal is resized.
    # Currently not working right.
    def resize(self,newH,newW):
        newY,newX = screen.getmaxyx()
        self.window.resize(newH, newW)
        self.window.box()
        self.window.refresh()

def main(screen):
    duck = Pet('Ducksu')
    while True:
        #resize = curses.is_term_resized(maxY, maxX)

        win.top_left = MenuWindow('', int(maxY / 2), int(maxX / 2), 0, 0)
        win.top_left.addstr(duck.placeIcon()[0], duck.placeIcon()[1], duck.placeIcon()[2])
        win.bot_left = MenuWindow('Bottom Left', int(maxY / 2), int(maxX / 2), int(maxY / 2), 0)
        win.right = MenuWindow('Right Side', int(maxY), int(maxX / 2), 0, int(maxX / 2))

        win.top_left.refresh()
        win.bot_left.refresh()
        win.right.refresh()
        curses.napms(500)

        duck.direction = random.choice(DIRECTION)
        duck.facing()
        duck.waddle()

        #curses.napms(3000)

        #if resize is True:
        #    win.top_left.resize(int(maxY / 2), int(maxX / 2))
        #    win.bot_left.resize(int(maxY / 2), int(maxX / 2))
        #    win.right.resize(int(maxY), int(maxX / 2))



wrapper(main)