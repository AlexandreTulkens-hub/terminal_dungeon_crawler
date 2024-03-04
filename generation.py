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


class DungeonGenerator:

    def __init__(self, params: argparse.Namespace):
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
        self.bonuses = params.bonuses

    def create_rooms_coordinates(self):
        """
        Creates a list of all the room coordinates to be used in generate()

        :return: list of all the room coordinates
        :rtype: List[List[Pos2D]]
        """
        nb_rooms = self.rooms
        rooms_coordinates = set()
        # max coordinates of tl corner of a room
        x_max = self.width - self.minwidth - 2  # - 2 because room needs distance of 1 with grid borders
        y_max = self.height - self.minheight - 2  # and because inclusive range of randint
        for i in range(nb_rooms):
            room = tuple()
            found = False
            while not found:
                x_tl = random.randint(2, x_max)
                y_tl = random.randint(1, y_max)
                # take the min because sometimes bottom right corner will surpass the borders of grid
                x_br = random.randint(x_tl + self.minwidth, min(x_tl + self.maxwidth, self.width - 2))
                y_br = random.randint(y_tl + self.minheight, min(y_tl + self.maxheight, self.height - 2))

                room = (Pos2D(x_tl, y_tl), Pos2D(x_br, y_br))
                if not any(rooms_overlapping(existing_room, room) for existing_room in rooms_coordinates):
                    found = True

            rooms_coordinates.add(room)

        return rooms_coordinates

    def create_bonus_coordinates(self):
        """
        list of all bonuses

        :rtype: List[Pos2D]
        """
        bonuses_list = []
        for _ in range(self.bonuses):
            bonus = Pos2D(random.randint(0, self.width-1), random.randint(0, self.height-1))
            while bonus in bonuses_list:
                bonus = Pos2D(random.randint(0, self.width-1), random.randint(0, self.height-1))
            bonuses_list.append(bonus)

        return bonuses_list


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
        Generates a dungeon with its rooms, its player and its exit

        :return: A dictionary with the following keys and values:
             - 'grid': (Grid) the grid containing the dungeon.
             - 'bonuses': (list[Pos2D]) coordinates of all lamp recharges
             - 'start_position': (Pos2D) coordinates of starting position of player
             - 'exit_position' : (Pos2D) coordinates of dungeon exit
        :rtype: dict
        """
        dungeon = Grid(self.width, self.height)  # create empty dungeon
        rooms = []  # going to contain all the rooms
        room_coordinates = self.create_rooms_coordinates()  # create room coordinates
        bonus_list = self.create_bonus_coordinates()  # create position of bonuses

        # create and add rooms to dungeon
        for coordinate in room_coordinates:
            rooms.append(Box(coordinate[0], coordinate[1]))
            dungeon.isolate_box(rooms[-1])
        if self.hard:
            dungeon = dungeon.spanning_tree()
        else:
            # create the two mazes that will get merged
            span1 = dungeon.spanning_tree()
            span2 = dungeon.spanning_tree()

            dungeon = self.merge_spanning_tree(span1, span2)

        # create the entrances/exits
        for room in rooms:
            for i in range(self.openings):
                opening = room.opening_coordinates()
                dungeon.remove_wall(opening[0], opening[1])

        # create starting position of player and exit position of dungeon
        start_pos = Pos2D(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        exit_pos = Pos2D(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        while start_pos in bonus_list or start_pos == exit_pos:
            start_pos = Pos2D(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            exit_pos = Pos2D(random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        return {'grid': dungeon, 'bonuses': bonus_list, 'start_position': start_pos, 'exit_position': exit_pos}


def rooms_overlapping(existing_r: tuple[Pos2D, Pos2D], r: tuple[Pos2D, Pos2D]):
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
