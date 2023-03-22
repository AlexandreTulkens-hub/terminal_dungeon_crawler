import argparse
from generation import DungeonGenerator
from renderer import GridRenderer

parser = argparse.ArgumentParser(description='Create a DungeonGenerator object')

arguments = {'width': {'type': int, 'help': 'Width of the dungeon'},
             'height': {'type': int, 'help': 'Height of the dungeon'},
             '--rooms': {'default': 3, 'type': int, 'help': 'Number of rooms to generate (default: 5)'},
             '--seed': {'default': None, 'type': int, 'help': 'Seed for RNG (default: None)'},
             '--minwidth': {'default': 4, 'type': int, 'help': 'Min width of a room (default: 4)'},
             '--maxwidth': {'default': 8, 'type': int, 'help': 'Max width of a room (default: 8)'},
             '--minheight': {'default': 4, 'type': int, 'help': 'Min height of a room (default: 4)'},
             '--maxheight': {'default': 8, 'type': int, 'help': 'Max height of a room (default: 8)'},
             '--openings': {'default': 2, 'type': int, 'help': 'Number of openings per room (default: 2)'},
             '--hard': {'default': False, 'type': bool, 'help': 'Specify that dungeon is based on maze,\
                        not on merge of two trees'},
             '--view-radius': {'default': 6, 'type': int, 'help': 'visible radius of dungeon'},
             '--bonuses': {'default': 2, 'type': int, 'help': 'bonuses to recharge lamp'},
             '--bonus-radius': {'default': 3, 'type': int, 'help': 'the recharge of the bonus'},
             '--torch-delay': {'default': 7, 'type': int, 'help': 'nb of movements before lamp burns out'}}
# add the arguments to parser
for arg, properties in arguments.items():
    parser.add_argument(arg, **properties)

generator = DungeonGenerator(parser.parse_args())
dungeon_test = generator.generate()['grid']
render = GridRenderer(dungeon_test)
render.show()