#!/usr/bin/python3
import curses, random
# import sys, tty
from curses import wrapper

screen = curses.initscr()
maxY, maxX = screen.getmaxyx()
curses.curs_set(0)

DIRECTION = ["RIGHT", "LEFT", "UP", "DOWN"]
WORM_OBJS = []

class win:
    pass

class Worm:

    def __init__(self, posY, posX, icon = "~"):
        self.posY = posY
        self.posX = posX
        self.position = [posY, posX]
        self.icon = icon

    def setWorm(self):
        return self.posY, self.posX, self.icon

class Pet:
    maxY, maxX = screen.getmaxyx()
    def __init__(self, name, direction = "RIGHT", posY = 1, posX = 1):
        self.name = name
        self.direction = direction
        self.position = [posY, posX]
        self.posY = posY
        self.posX = posX
        self.icon = "d"

    def peck(self):
        pass

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

    def addch(self, y, x, char, attr=0):
        self.window.addch(y, x, char, attr)

    def delch(self, y, x):
        self.window.delch(y,x)

    # Resize windows when terminal is resized.
    # Currently not working right.
    def resize(self,newH,newW):
        newY,newX = screen.getmaxyx()
        self.window.resize(newH, newW)
        self.window.box()
        self.window.refresh()

def makeWorm(maxY, maxX):
    randY, randX = random.randrange(1, int(maxY/2-2)), random.randrange(1, int(maxX/2-2))
    worm_obj = Worm(randY, randX)
    WORM_OBJS.append(worm_obj)

def main(screen):
    duck = Pet('Ducksu')
    wormsEaten = 0
    while True:
        #resize = curses.is_term_resized(maxY, maxX)

        win.top_left = MenuWindow(str(wormsEaten), int(maxY / 2), int(maxX / 2), 0, 0)
        win.top_left.addstr(duck.placeIcon()[0], duck.placeIcon()[1], duck.placeIcon()[2])
        win.bot_left = MenuWindow('Bottom Left', int(maxY / 2), int(maxX / 2), int(maxY / 2), 0)
        win.right = MenuWindow('Right Side', int(maxY), int(maxX / 2), 0, int(maxX / 2))

        win.top_left.refresh()
        win.bot_left.refresh()
        win.right.refresh()

        if random.randrange(0,50) >= 40 and len(WORM_OBJS) < 5:
            makeWorm(maxY, maxX)

        for i in WORM_OBJS:
            if duck.posY == i.posY and duck.posX == i.posX:
                duck.peck()
                wormsEaten += 1
                win.top_left.delch(i.posY, i.posX)
                WORM_OBJS.remove(i)
                win.top_left.refresh()
                break

            win.top_left.addstr(i.setWorm()[0], i.setWorm()[1], i.setWorm()[2])

            win.top_left.refresh()


        curses.napms(250)

        duck.direction = random.choice(DIRECTION)
        duck.facing()
        duck.waddle()

        #curses.napms(3000)

        #if resize is True:
        #    win.top_left.resize(int(maxY / 2), int(maxX / 2))
        #    win.bot_left.resize(int(maxY / 2), int(maxX / 2))
        #    win.right.resize(int(maxY), int(maxX / 2))

wrapper(main)