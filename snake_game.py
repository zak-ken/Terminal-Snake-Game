import random
import curses
import os
import time
import copy

"""
STEPS
# S1: Walls
# S2: Character that moves
# S3: Character cannot go through walls

OBSTACLES
* moving walls 
* Bullets that slow you

"""


class Character(object):
    prev_position = character_position = Ycenter = Mheight = Mwidth = window = None

    def generate_character(self):
        self.window.addch(self.Ycenter, 5, '*')
        self.character_position = [self.Ycenter, 5]
        self.prev_position = copy.copy(self.character_position)
        self.window.refresh()

    def del_character_position(self):
        self.window.addch(self.prev_position[0], self.prev_position[1], ' ')

    def set_new_character_position(self):
        self.window.addch(self.character_position[0], self.character_position[1], '*')

    def update_prev_character_position(self):
        self.prev_position = copy.copy(self.character_position)

    def CheckCollision(self):
        pass


class GenerateMap(object):
    """
        This function handles wall and trap creation, and map collision
    """
    Ycenter = Mheight = Mwidth = window = None
    walls = set()

    def generate_map(self):
        path_height = (self.Ycenter // 6)
        for i in range(self.Mwidth):
            self.window.addch(self.Ycenter + path_height, i, '=')
            self.window.addch(self.Ycenter - path_height, i, '=')
            self.walls.add((self.Ycenter + path_height, i))
            self.walls.add((self.Ycenter - path_height, i))

        self.window.refresh()

    def traps(self):
        pass

    def move_wave(self):
        """
            Generates a wave that eventually fully closes the path, if the character touches it he dies
        """



        pass


class Game(GenerateMap, Character):  # what is the minimum size for the screen?

    def __init__(self):
        self.Scrn = curses.initscr()
        self.Scrn.timeout(100)
        self.Mheight, self.Mwidth = self.Scrn.getmaxyx()
        self.window = curses.newwin(self.Mheight, self.Mwidth, 0, 0)  # Creates the new window for the Cursor overlay
        self.window.keypad(True)  # Treats special keys as special values e.g. character key to ASCII number
        self.window.timeout(100)  # Slows down the loop that check for keys that are pressed

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.keypad(False)
        curses.noecho()
        curses.cbreak()
        curses.endwin()
        os.system('stty sane')
        quit()

    def __enter__(self):
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        return self

    def start(self):
        # Collision checks are done here
        while True:
            update = False
            key = self.window.getch()  # This does a self.window.refresh()
            if key == curses.KEY_UP:
                self.character_position[0] -= 1
                update = True
            elif key == curses.KEY_DOWN:
                self.character_position[0] += 1
                update = True
            elif key == curses.KEY_LEFT:
                self.character_position[1] -= 1
                update = True
            elif key == curses.KEY_RIGHT:
                self.character_position[1] += 1
                update = True

            if (self.character_position[0], self.character_position[1]) in self.walls:
                self.character_position = copy.copy(self.prev_position)
                continue

            if update:
                self.del_character_position()
                self.update_prev_character_position()
                self.set_new_character_position()

            self.move_wave()


    # New methods/properties should be made for mutations
    @property
    def Xcenter(self):
        return self.Mwidth // 2

    @property
    def Ycenter(self):
        return self.Mheight // 2


if "__main__" == __name__:
    with Game() as game:
        game.generate_map()
        game.generate_character()
        game.start()
