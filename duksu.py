#!/usr/bin/python3
import curses
import math
import random
from curses import wrapper
from dataclasses import dataclass

screen = curses.initscr()
max_y, max_x = screen.getmaxyx()
curses.curs_set(0)

worm_object_list = []

@dataclass
class Animal:
    Y_position: int
    X_position: int
    icon: str

    def set_animal(self):
        return self.Y_position, self.X_position, self.icon


@dataclass
class Worm(Animal):
    """Worms that Duksu can eat."""
    
    distance = float('inf')

    # Create worm objects and store it in WORM_OBJ list.
    @classmethod
    def make_worm(cls,winObject):
        worm_icon = '~'
        random_Y, random_X = random.randrange(2, winObject.height - 2), random.randrange(2, winObject.width - 2)
        return cls(random_Y, random_X, worm_icon)


@dataclass
class Duck(Animal):
    """Pet duck that wanders around the screen and pecks at worms.
    Future features include 'talking' with owner, splashing in a pond,
    having a 'hunger meter' and needing to be fed by owner."""

    DIRECTIONS = ["RIGHT", "LEFT", "UP", "DOWN"]
    direction = "RIGHT"

    #Duksu stats
    worms_eaten = 0
    hunger = 0
    boredom = 0

    def duck_action(self, winObject):
        winObject.addstr(self.Y_position, self.X_position, ' ')
        if worm_object_list:
            for worm in worm_object_list:
                self.detect_worm(worm)

        if not worm_object_list or not worm_object_list[0].distance <= 10 :
            self.facing()
            self.waddle(winObject)

        elif self.Y_position == worm_object_list[0].Y_position and self.X_position == worm_object_list[0].X_position:
            self.peck(worm_object_list[0], winObject)
            self.facing()
            self.waddle(winObject)

        elif worm_object_list[0].distance <= 10 :
            self.move_towards_worm(worm_object_list[0], winObject)

    def detect_worm(self, wormObject): 
        """Check if Duksu sees any worms."""
        distance = math.sqrt((self.X_position - wormObject.X_position) ** 2 + (self.Y_position - wormObject.Y_position) ** 2)
        if distance <= 10:
            wormObject.distance = distance
            worm_object_list.sort(key = lambda x: x.distance)

    def move_towards_worm(self, closestWorm, winObject):
        """Move the duck object towards the closest worm object"""
        if closestWorm.X_position > self.X_position and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif closestWorm.X_position < self.X_position and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif closestWorm.Y_position > self.Y_position and self.direction != "UP":
            self.direction = "DOWN"
        elif closestWorm.Y_position < self.Y_position and self.direction != "DOWN":
            self.direction = "UP"
        self.waddle(winObject)


    def peck(self, wormObject, winObject):
        """Increments worms_eaten, removes worm from screen and from worm_object_list"""
        self.worms_eaten += 1
        winObject.addstr(wormObject.Y_position, wormObject.X_position, ' ')
        worm_object_list.remove(wormObject)

    def facing(self):
        """Set the direction that Duksu is facing"""
        if self.Y_position and self.X_position == 1:
            self.direction = random.choice(["RIGHT", "DOWN"])
        elif self.Y_position == 1 and self.X_position != 1:
            self.direction = random.choice(["RIGHT", "LEFT", "DOWN"])
        elif self.Y_position != 1 and self.X_position == 1:
            self.direction = random.choice(["RIGHT", "UP", "DOWN"])
        else:
            self.direction = random.choice(self.DIRECTIONS)

    def waddle(self, winObject):
        """Move Duksu one square in the direction he is facing, within window boundary"""
        if self.X_position < winObject.width - 2 and self.direction == "RIGHT":
            self.prevX = self.X_position
            self.X_position += 1
            Animal.set_animal(self)
        elif self.X_position > 1 and self.direction == "LEFT":
            self.prevX = self.X_position
            self.X_position -= 1
            Animal.set_animal(self)
        elif self.Y_position > 1 and self.direction == "UP":
            self.prevY = self.Y_position
            self.Y_position -= 1
            Animal.set_animal(self)
        elif self.Y_position < winObject.height - 2 and self.direction == "DOWN":
            self.prevY = self.Y_position
            self.Y_position += 1
            Animal.set_animal(self)

    def increase_hunger(self):
        self.hunger += 1

    def increase_boredom(self):
        self.boredom += 1


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
        for y in range(3, self.window.getmax_yx()[0] - 1):
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


def mode_input(winObject1, mode):
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
    else:
        return mode


def refresh_screen(fieldWinObject, statsWinObject):
    fieldWinObject.refresh()
    statsWinObject.refresh()

def draw_field(winObject, duckObj, wormObj):
    winObject.addstr(*duckObj.set_animal())
    if wormObj:
        for worm in wormObj:
            winObject.addstr(*worm.set_animal())

def draw_stats(statsObject, duckObject):
    statsObject.addstr(0, statsObject.width // 2, 'Duksu')
    statsObject.addstr(2,2, 'Worms Eaten:' + str(duckObject.worms_eaten))
    statsObject.addstr(3,2, 'Hunger:' + str(duckObject.hunger))

def draw_game_windows(field_object, stats_object, duck_object, worm_object):
    draw_stats(stats_object, duck_object)
    draw_field(field_object, duck_object, worm_object)
    refresh_screen(field_object, stats_object)

# Main function with curses screen passed to it for Wrapper()
def main(screen):
    mode = 'RUN'

    # Initialize Curses windows
    field = Windows('', int(max_y), int(max_x - (max_x / 3)), 0, 0)
    stats = Windows('', int(max_y), int(max_x / 3), 0, int(max_x - (max_x / 3)))
    duksu = Duck(field.height // 2, field.width // 2, 'D')
    
    while mode == 'RUN':
        mode = mode_input(field, mode)

        draw_game_windows(field, stats, duksu, worm_object_list)

        # ~2% chance to spawn a worm if less than 5 worms are present every 'tick', 
        if random.randrange(0, 1000) <= 20 and len(worm_object_list) < 5:
            worm_object_list.append(Worm.make_worm(field))

        duksu.duck_action(field)

        curses.napms(750)  # 1 'tick' = 750 ms [MUST BE AFTER refresh_screen FOR SOME REASON]
# Call main through curses.wrapper
wrapper(main)
