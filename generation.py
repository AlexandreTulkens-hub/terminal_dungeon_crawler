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
from renderer import GridRenderer


def rooms_overlapping(existing_r: Pos2D, r: Pos2D):
    """
    verifies if 2 rooms overlap or not

    :param existing_r: room that already exists
    :param r: new potential room
    :return: True if the new potential room can't be created, False otherwise
    :rtype: bool
    """
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

        self.rooms = params.rooms
        self.seed = params.seed
        self.minwidth = params.minwidth
        self.maxwidth = params.maxwidth
        self.minheight = params.minheight
        self.maxheight = params.maxheight
        self.openings = params.openings
        self.hard = params.hard
        self.width = params.width
        self.height = params.height

    def create_rooms_coordinates(self):
        """
        Creates a list of all the room coordinates to be used in generate()

        :return: list of all the room coordinates
        :rtype: List[List[Pos2D]]
        """
        nb_rooms = self.rooms
        rooms_coordinates = set()
        # max coordinates of tl corner of a room
        x_max = self.width - self.minwidth - 2  # - 2 because room need to have a distance of 1 with the borders of grid
        y_max = self.height - self.minheight - 2
        for i in range(nb_rooms):
            room = tuple()
            found = False
            while not found:
                x_tl = random.randint(1, x_max)
                y_tl = random.randint(1, y_max)
                # take the min because sometimes bottom right corner will surpass the borders of grid
                x_br = random.randint(x_tl + self.minwidth, min(x_tl + self.maxwidth, self.width - 2))
                y_br = random.randint(y_tl + self.minheight, min(y_tl + self.maxheight, self.height - 2))

                room = (Pos2D(x_tl, y_tl), Pos2D(x_br, y_br))
                if not any(rooms_overlapping(existing_room, room) for existing_room in rooms_coordinates):
                    found = True

            rooms_coordinates.add(room)

        return rooms_coordinates

    def merge_spanning_tree(self, span1: Grid, span2: Grid):
        """
        Merges the two mazes together by keeping the walls in common

        :param span1: first generated maze using dfs
        :param span2: second generated maze using dfs
        :return dungeon: the dungeon without the entrances
        :rtype: Grid
        """
        dungeon = Grid(self.width, self.height)
        for row in range(self.height):
            for column in range(self.width):
                if not span1[row, column].up and not span2[row, column].up:
                    dungeon[row, column].up = False
                if not span1[row, column].down and not span2[row, column].down:
                    dungeon[row, column].down = False
                if not span1[row, column].left and not span2[row, column].left:
                    dungeon[row, column].left = False
                if not span1[row, column].right and not span2[row, column].right:
                    dungeon[row, column].right = False
        return dungeon

    def generate(self):
        """
        Generates a dungeon with its rooms, its maze and its exits

        :return:A dictionary with the following keys and values:
             - 'grid': (Grid) the grid containing the dungeon.
        :rtype: dict
        """
        dungeon = Grid(self.width, self.height)  # create empty dungeon
        boxes = []  # going to contain all the rooms
        rooms = self.create_rooms_coordinates()  # create rooms
        # add rooms to dungeon
        counter = 0
        for room in rooms:
            boxes.append(Box(room[0], room[1]))
            dungeon.isolate_box(boxes[counter])
            counter += 1
        if self.hard:
            dungeon = dungeon.spanning_tree()
        else:
            # create the two mazes that will get merged
            span1 = dungeon.spanning_tree()
            GridRenderer(span1).show()
            span2 = dungeon.spanning_tree()
            GridRenderer(span2).show()

            dungeon = self.merge_spanning_tree(span1, span2)

        # create the entrances/exits
        for box in boxes:
            opening = box.opening_coordinates()
            dungeon.remove_wall(opening[0], opening[1])

        return {'grid': dungeon}
