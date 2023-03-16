"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
import argparse
import random
from grid import Grid
from pos2d import Pos2D
from box import Box


def rooms_overlapping(existing_r, r):
    ex_tl_x = existing_r[0].x - 2
    ex_tl_y = existing_r[0].y - 2
    ex_br_x = existing_r[1].x + 2
    ex_br_y = existing_r[1].y + 2

    # Check for horizontal overlap
    if ex_tl_x <= r[1].x and ex_br_x >= r[0].x:
        # Check for vertical overlap
        if ex_tl_y <= r[1].y and ex_br_y >= r[0].y:
            return True
    return False


class DungeonGenerator:

    def __init__(self, params: argparse.Namespace):
        parser = argparse.ArgumentParser(description='Create a DungeonGenerator object')

        arguments = {'width': {'help': 'Width of the dungeon'},
                     'height': {'help': 'Height of the dungeon'},
                     '--rooms': {'default': 5, 'help': 'Number of rooms to generate (default: 5)'},
                     '--seed': {'default': None, 'help': 'Seed for RNG (default: None)'},
                     '--minwidth': {'default': 4, 'help': 'Min width of a room (default: 4)'},
                     '--maxwidth': {'default': 8, 'help': 'Max width of a room (default: 8)'},
                     '--minheight': {'default': 4, 'help': 'Min height of a room (default: 4)'},
                     '--maxheight': {'default': 8, 'help': 'Max height of a room (default: 8)'},
                     '--openings': {'default': 2, 'help': 'Number of openings per room (default: 2)'}}
        # add the arguments to parser
        for arg, properties in arguments.items():
            parser.add_argument(arg, **properties)

        self.width = params.width
        self.height = params.height
        self.rooms = params.rooms
        self.seed = params.seed
        self.minwidth = params.minwidth
        self.maxwidth = params.maxwidth
        self.minheight = params.minheight
        self.maxheight = params.maxheight
        self.openings = params.openings
        self.hard = params.hard

    def create_rooms_coordinates(self):
        """
        Creates a list of all the room coordinates to be used in generate()

        :return: list of all the room coordinates
        :rtype: List[List[Pos2D]]
        """
        nb_rooms = self.rooms
        rooms_coordinates = []
        # max coordinates of tl corner of a room
        x_max = self.width - self.minwidth - 2  # - 2 because room need to have a distance of 1 with the borders of grid
        y_max = self.height - self.minheight - 2
        for i in range(nb_rooms):
            room = []
            found = False
            while not found:
                x_tl = random.randint(1, x_max)
                y_tl = random.randint(1, y_max)
                # take the min because sometimes bottom right corner will surpass the borders of grid
                x_br = random.randint(x_tl + self.minwidth, min(x_tl + self.maxwidth, self.width - 2))
                y_br = random.randint(y_tl + self.minheight, min(y_tl + self.maxheight, self.height - 2))

                room = [Pos2D(x_tl, y_tl), Pos2D(x_br, y_br)]
                if not any(rooms_overlapping(existing_room, room) for existing_room in rooms_coordinates):
                    found = True

            rooms_coordinates.append(room)

        return rooms_coordinates

    def generate(self):
        """
        Generates a dungeon with its rooms, its maze and its exits

        :return:A dictionary with the following keys and values:
             - 'grid': (Grid) the grid containing the dungeon.
        :rtype: dict
        """
        grid = Grid(self.width, self.height)
        if self.hard:
            grid = grid.spanning_tree()
        else:
            rooms = self.create_rooms_coordinates()
            # create rooms
            for element in rooms:
                room = Box(element[0], element[1])
                grid.isolate_box(room)
        return {'grid': grid}
