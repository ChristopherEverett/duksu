#!/usr/bin/python3
import curses
import random
from curses import wrapper

screen = curses.initscr()
maxY, maxX = screen.getmaxyx()
curses.curs_set(0)

DIRECTION = ["RIGHT", "LEFT", "UP", "DOWN"]
WORM_OBJS = []


class Win:
    pass


class Worm:

    def __init__(self, posY, posX, icon="~"):
        self.posY = posY
        self.posX = posX
        self.position = [posY, posX]
        self.icon = icon

    def setWorm(self):
        return self.posY, self.posX, self.icon


class Pet:
    def __init__(self, name, direction="RIGHT", posY=1, posX=1):
        self.name = name
        self.direction = direction
        self.position = [posY, posX]
        self.posY = posY
        self.posX = posX
        self.icon = "D"
        self.wormsEaten = 0

    def peck(self, wormObject, winObject):
        self.wormsEaten += 1
        winObject.delch(wormObject.posY, wormObject.posX)
        WORM_OBJS.remove(wormObject)

    def facing(self):
        if self.direction == "RIGHT" or self.direction == "UP":
            self.icon = "D"
        else:
            self.icon = "ᗡ"

    def waddle(self, winObject):
        if self.posX < winObject.width - 2 and self.direction == "RIGHT":
            self.posX += 1
            return self.posY, self.posX
        elif self.posX > 1 and self.direction == "LEFT":
            self.posX -= 1
            return self.posY, self.posX
        elif self.posY > 1 and self.direction == "UP":
            self.posY -= 1
            return self.posY, self.posX
        elif self.posY < winObject.height - 2 and self.direction == "DOWN":
            self.posY += 1
            return self.posY, self.posX

    def placeIcon(self):
        return self.posY, self.posX, self.icon


class MenuWindow:
    def __init__(self, title, h, w, y, x):
        self.window = curses.newwin(h, w, y, x)
        self.height = h
        self.width = w
        self.window.nodelay(True)
        self.window.box()
        self.window.addstr(1, 2, title)
        self.window.refresh()

    def refresh(self):
        self.window.refresh()

    def clear(self):
        for y in range(3, self.window.getmaxyx()[0] - 1):
            self.window.move(y, 2)
            self.window.clrtoeol()
        self.window.box()

    def addstr(self, y, x, string, attr=0):
        self.window.addstr(y, x, string, attr)

    def addch(self, y, x, char, attr=0):
        self.window.addch(y, x, char, attr)

    def delch(self, y, x):
        self.window.delch(y, x)


def makeWorm(winObject):
    randY, randX = random.randrange(1, winObject.height - 2), random.randrange(1, winObject.width - 2)
    WORM_OBJS.append(Worm(randY, randX))

# Main function with curses screen passed to it for Wrapper()
def main(screen):
    duck = Pet('Ducksu')
    while True:
        # Initialize Curses windows
        Win.top_left = MenuWindow('', int(maxY / 2), int(maxX / 2), 0, 0)
        Win.bot_left = MenuWindow('Bottom Left', int(maxY / 2), int(maxX / 2), int(maxY / 2), 0)
        Win.right = MenuWindow('Worms Eaten: ' + str(duck.wormsEaten), int(maxY), int(maxX / 2), 0, int(maxX / 2))

        # Place Duck in Top Left window
        Win.top_left.addstr(duck.placeIcon()[0], duck.placeIcon()[1], duck.placeIcon()[2])

        # Refresh all windows
        Win.top_left.refresh()
        Win.bot_left.refresh()
        Win.right.refresh()

        # ~2% chance to spawn a worm if less than 5 worms are present every 'tick'
        if random.randrange(0, 1000) <= 80 and len(WORM_OBJS) < 5:
            makeWorm(Win.top_left) # Worm objects are stored in the global list WORM_OBJS

        # Iterate through worm objects
        for i in WORM_OBJS:
            # Check if duck and worm are on the same square
            if duck.posY == i.posY and duck.posX == i.posX:
                duck.peck(i, Win.top_left) # Increments 'wormsEaten', deletes '~' from current position, then removes worm object from WORM_OBJ
                Win.top_left.refresh()
                break

            # Draw '~' at random y,x within top left window, then update window.
            Win.top_left.addstr(i.setWorm()[0], i.setWorm()[1], i.setWorm()[2])

            Win.top_left.refresh()

        # 1 'tick' = 750 ms
        curses.napms(750)

        # Set direction duck is facing, change icon, move 1 square in that direction (Try putting 'DIRECTION' in Pet class)
        duck.direction = random.choice(DIRECTION)
        duck.facing()
        duck.waddle(Win.top_left)

# Call main through curses.wrapper
wrapper(main)
