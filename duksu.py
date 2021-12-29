#!/usr/bin/python3
import curses
import random
from curses import wrapper

screen = curses.initscr()
maxY, maxX = screen.getmaxyx()
curses.curs_set(0)

WORM_OBJS = []


class Win:
    pass


class Worm:
    """Worms that Duksu can eat."""
    def __init__(self, posY, posX, icon="~"):
        self.posY = posY
        self.posX = posX
        self.position = [posY, posX]
        self.icon = icon

    # Return Worm's position and '~'
    def setWorm(self):
        return self.posY, self.posX, self.icon


class Pet:
    """Pet duck that wanders around the screen and pecks at worms.
    Future features include 'talking' with owner, splashing in a pond,
    having a 'hunger meter' and needing to be fed by owner."""

    DIRECTIONS = ["RIGHT", "LEFT", "UP", "DOWN"]

    def __init__(self, name, posY=1, posX=1):
        self.name = name
        self.direction = "RIGHT"
        self.position = [posY, posX]
        self.posY = posY
        self.posX = posX
        self.icon = "D"
        self.wormsEaten = 0

    # Increments wormsEaten, removes worm from screen and from WORM_OBJS
    def peck(self, wormObject, winObject):
        self.wormsEaten += 1
        winObject.delch(wormObject.posY, wormObject.posX)
        WORM_OBJS.remove(wormObject)

    # Change which direction duck is facing.
    def facing(self):
        self.direction = random.choice(self.DIRECTIONS)

        if self.direction == "RIGHT" or self.direction == "UP":
            self.icon = "D"
        else:
            self.icon = "ᗡ"

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


class MenuWindow:
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
    randY, randX = random.randrange(1, winObject.height - 2), random.randrange(1, winObject.width - 2)
    WORM_OBJS.append(Worm(randY, randX))


# Main function with curses screen passed to it for Wrapper()
def main(screen):
    duck = Pet('Ducksu')
    run = True
    while run:
        # Initialize Curses windows
        Win.top_left = MenuWindow('', int(maxY), int(maxX - (maxX / 3)), 0, 0)
        Win.right = MenuWindow('Worms Eaten: ' + str(duck.wormsEaten), int(maxY), int(maxX / 3), 0, int(maxX - (maxX / 3)))

        ch = Win.top_left.getch()
        if ch == 27:
            run = False
        else:

            # Place Duck in Top Left window
            Win.top_left.addstr(duck.placeIcon()[0], duck.placeIcon()[1], duck.placeIcon()[2])

            # Refresh all windows
            Win.top_left.refresh()
            Win.right.refresh()

            # ~2% chance to spawn a worm if less than 5 worms are present every 'tick'
            if random.randrange(0, 1000) <= 20 and len(WORM_OBJS) < 5:
                makeWorm(Win.top_left)  # Worm objects are stored in the global list WORM_OBJS

            # Iterate through worm objects
            for i in WORM_OBJS:
                # Check if duck and worm are on the same square
                if duck.posY == i.posY and duck.posX == i.posX:
                    duck.peck(i, Win.top_left)  # Increments 'wormsEaten', deletes '~' from position, removes worm object from WORM_OBJ
                    Win.top_left.refresh()
                    break

                # Draw '~' at random y,x within top left window, then update window.
                Win.top_left.addstr(i.setWorm()[0], i.setWorm()[1], i.setWorm()[2])

                Win.top_left.refresh()

            # 1 'tick' = 750 ms
            curses.napms(750)

            # Set direction duck is facing, change icon, move 1 square in that direction
            duck.facing()
            duck.waddle(Win.top_left)




# Call main through curses.wrapper
wrapper(main)
