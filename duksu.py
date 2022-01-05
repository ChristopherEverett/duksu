#!/usr/bin/python3
import curses
import random
from curses import wrapper
from dataclasses import dataclass

screen = curses.initscr()
maxY, maxX = screen.getmaxyx()
curses.curs_set(0)

WORM_OBJS = []


@dataclass
class Animal:
    posY: int
    posX: int
    icon: str


@dataclass
class Worm(Animal):
    """Worms that Duksu can eat."""

    # Return Worm's position and '~'
    def setWorm(self):
        return self.posY, self.posX, self.icon


@dataclass
class Duck(Animal):
    """Pet duck that wanders around the screen and pecks at worms.
    Future features include 'talking' with owner, splashing in a pond,
    having a 'hunger meter' and needing to be fed by owner."""

    DIRECTIONS = ["RIGHT", "LEFT", "UP", "DOWN"]
    direction = "RIGHT"
    wormsEaten = 0
    hunger = 0
    fun = 100

    # Increments wormsEaten, removes worm from screen and from WORM_OBJS
    def peck(self, wormObject, winObject):
        self.wormsEaten += 1
        winObject.addstr(wormObject.posY, wormObject.posX, ' ')
        WORM_OBJS.remove(wormObject)

    # Change which direction duck is facing.
    def facing(self):
        self.direction = random.choice(self.DIRECTIONS)

    # Move around screen depending on direction faced, making sure it is within windows boundary.
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

    # Returns Duck position and 'D' or 'ᗡ' depending on facing.
    def placeIcon(self):
        return self.posY, self.posX, self.icon


class Windows:
    """Set up curses windows in certain sizes with 'window decorations' """

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

    def getch(self):
        return self.window.getch()

    def delch(self, y, x):
        self.window.delch(y, x)


# Create worm objects and store it in WORM_OBJ list. Try to put this in Worm class.
def makeWorm(winObject):
    randY, randX = random.randrange(2, winObject.height - 2), random.randrange(2, winObject.width - 2)
    WORM_OBJS.append(Worm(randY, randX, '~'))


def modeInput(winObject, mode):
    ch = winObject.getch()

    # Exit program if ESC is pressed
    if ch == 27:
        return 'STOP'
    # If ENTER is pressed, check if in RUN or MENU mode, toggle between the two.
    elif ch == 10:
        if mode == 'RUN':
            return 'MENU'
        else:
            return 'RUN'
    # If nothing is pressed, return current mode.
    elif ch == -1:
        return mode


# Main function with curses screen passed to it for Wrapper()
def main(screen):
    duck = Duck(1, 1, 'D')
    mode = 'RUN'

    # Initialize Curses windows
    top_left = Windows('', int(maxY), int(maxX - (maxX / 3)), 0, 0)
    right = Windows('', int(maxY), int(maxX / 3), 0,
                    int(maxX - (maxX / 3)))

    # List Duck stats in right window
    right.addstr(0, right.width // 2, 'Duksu')

    while mode == 'RUN':

        mode = modeInput(top_left, mode)

        while mode == 'MENU':
            mode = modeInput(top_left, mode)
            right = Windows('Worms Eaten: ' + mode, int(maxY), int(maxX / 3), 0, int(maxX - (maxX / 3)))
            top_left.addstr(*duck.placeIcon())

            # Put code here to add menu options

            # Refresh all windows
            top_left.refresh()
            right.refresh()

        # Place Duck in Top Left window
        top_left.addstr(*duck.placeIcon())

        # Refresh all windows
        top_left.refresh()
        right.refresh()

        # ~2% chance to spawn a worm if less than 5 worms are present every 'tick'
        if random.randrange(0, 1000) <= 20 and len(WORM_OBJS) < 5:
            makeWorm(top_left)  # Worm objects are stored in the global list WORM_OBJS

        # Iterate through worm objects
        for i in WORM_OBJS:
            # Check if duck and worm are on the same square
            if duck.posY == i.posY and duck.posX == i.posX:
                # peck() increments 'wormsEaten', deletes '~' from position, removes worm object from WORM_OBJ
                duck.peck(i, top_left)
                top_left.refresh()
                break

            # Draw '~' at random y,x within top left window, then update window.
            top_left.addstr(*i.setWorm())
            top_left.refresh()

        # 1 'tick' = 750 ms
        curses.napms(50)

        # Set direction duck is facing, change icon, move 1 square in that direction
        top_left.addstr(duck.posY, duck.posX, ' ')
        duck.facing()
        duck.waddle(top_left)


# Call main through curses.wrapper
wrapper(main)
