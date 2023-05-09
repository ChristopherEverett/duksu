#!/usr/bin/python3
import curses
import math
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
    
    # Create worm objects and store it in WORM_OBJ list. Try to put this in Worm class.
    @classmethod
    def makeWorm(cls,winObject):
        wormIcon = '~'
        randY, randX = random.randrange(2, winObject.height - 2), random.randrange(2, winObject.width - 2)
        return cls(randY, randX, wormIcon)

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

    def detectWorm(self, wormObject):
            """Check if a worm is within 10 squares of the duck"""
            distance = math.sqrt((self.posX - wormObject.posX) ** 2 + (self.posY - wormObject.posY) ** 2)
            return distance <= 10

    def moveDuksu(self, winObject):
        """Move the duck object towards the closest worm object"""
        closest_worm = None
        min_distance = float('inf')
        for wormObject in WORM_OBJS:
            distance = math.sqrt((self.posX - wormObject.posX) ** 2 + (self.posY - wormObject.posY) ** 2)
            if distance < min_distance:
                closest_worm = wormObject
                min_distance = distance
        if closest_worm and min_distance <= 10:
            if closest_worm.posX > self.posX and self.direction != "LEFT":
                self.direction = "RIGHT"
                self.waddle(winObject)
            elif closest_worm.posX < self.posX and self.direction != "RIGHT":
                self.direction = "LEFT"
                self.waddle(winObject)
            elif closest_worm.posY > self.posY and self.direction != "UP":
                self.direction = "DOWN"
                self.waddle(winObject)
            elif closest_worm.posY < self.posY and self.direction != "DOWN":
                self.direction = "UP"
                self.waddle(winObject)
        else:
            self.facing()
            self.waddle(winObject)
        

    # Increments wormsEaten, removes worm from screen and from WORM_OBJS
    def peck(self, wormObject, winObject):
        """Increments wormsEaten, removes worm from screen and from WORM_OBJS"""
        self.wormsEaten += 1
        winObject.addstr(wormObject.posY, wormObject.posX, ' ')
        WORM_OBJS.remove(wormObject)

    # Change which direction duck is facing.
    def facing(self):
        """Set the direction that Duksu is facing"""
        if self.posY and self.posX == 1:
            self.direction = random.choice(["RIGHT", "DOWN"])
        elif self.posY == 1 and self.posX != 1:
            self.direction = random.choice(["RIGHT", "LEFT", "DOWN"])
        elif self.posY != 1 and self.posX == 1:
            self.direction = random.choice(["RIGHT", "UP", "DOWN"])
        else:
            self.direction = random.choice(self.DIRECTIONS)

    # Move around screen depending on direction faced, making sure it is within windows boundary.
    def waddle(self, winObject):
        """Move Duksu one square in the direction he is facing, within window boundary"""
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

def modeInput(winObject1, mode):
    ch = winObject1.getch()

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
 #   elif ch == -1:
  #      return mode
    else:
        return mode

def refreshScreen(fieldWinObject, menuWinObject):
    fieldWinObject.refresh()
    menuWinObject.refresh()

def drawMenu(winObject):
    winObject.addstr(0, winObject.width // 2, 'PAUSED')
 #   winObject.refresh()

def drawField(winObject, duckObj):
    winObject.addstr(*duckObj.placeIcon())

# Main function with curses screen passed to it for Wrapper()
def main(screen):
    duck = Duck(1, 1, 'D')
    mode = 'RUN'

    # Initialize Curses windows
    field = Windows('', int(maxY), int(maxX - (maxX / 3)), 0, 0)
    menu = Windows('', int(maxY), int(maxX / 3), 0,
                    int(maxX - (maxX / 3)))

    while mode == 'RUN':
        mode = modeInput(field, mode)

        # List Duck stats in menu window
        menu.addstr(0, menu.width // 2, 'Duksu')
        menu.addstr(2,2, 'Y,X:' + str(duck.posY) + ',' + str(duck.posX))

        while mode == 'MENU':
            mode = modeInput(field, mode)
            drawMenu(menu)
            drawField(field, duck)
            refreshScreen(field, menu)

        # Place Duck in Top Left window
        #field.addstr(*duck.placeIcon())
        drawField(field, duck)

        # Refresh all windows
        refreshScreen(field, menu)

        # ~2% chance to spawn a worm if less than 5 worms are present every 'tick'
        if random.randrange(0, 1000) <= 500 and len(WORM_OBJS) < 5:
            WORM_OBJS.append(Worm.makeWorm(field))


        # Iterate through worm objects
        for i in WORM_OBJS:
            # Check if duck and worm are on the same square
            if duck.posY == i.posY and duck.posX == i.posX:
                # peck() increments 'wormsEaten', deletes '~' from position, removes worm object from WORM_OBJ
                duck.peck(i, field)
                drawField(field, duck)
                field.refresh()
                break

            # Draw '~' at random y,x within top left window, then update window.
            field.addstr(*i.setWorm())
            field.refresh()

        # 1 'tick' = 750 ms
        curses.napms(50)

        # Check if worm is within 10 sq. of Duksu then move towards it one sq. Otherwise waddle in a random direction.
        field.addstr(duck.posY, duck.posX, ' ')
        if WORM_OBJS:
            duck.moveDuksu(field)
        else:
               duck.facing()
               duck.waddle(field)
# Call main through curses.wrapper
wrapper(main)
