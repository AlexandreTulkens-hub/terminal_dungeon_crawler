import argparse
import sys
import subprocess
import random
from generation import DungeonGenerator
from renderer import Renderer
from player import Player


def parse_arguments():
    """
    Define and parse command-line arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Parameters of Dungeon')

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
                 '--view-radius': {'default': 0, 'type': int, 'help': 'visible radius of dungeon'},
                 '--bonuses': {'default': 2, 'type': int, 'help': 'bonuses to recharge lamp'},
                 '--bonus-radius': {'default': 3, 'type': int, 'help': 'How much lamp recharges'},
                 '--torch-delay': {'default': 7, 'type': int, 'help': 'nb of movements before lamp burns out'}}
    # add the arguments to parser
    for arg, properties in arguments.items():
        parser.add_argument(arg, **properties)

    # parse the arguments and return the parsed arguments
    return parser.parse_args()


def clear_terminal():
    """
    Clears terminal to make the game more immersive
    :return: None
    """
    # Use ANSI escape codes to clear the terminal screen
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()


def relaunch_script(args):
    """
    Relaunches the script
    :param args: command line arguments(options of the game)
    :return: None
    """
    # Get the command used to run the script
    command = [sys.executable] + [sys.argv[0]]

    print(vars(args).items())
    # Generate command-line arguments for modified values
    for arg_name, arg_value in vars(args).items():
        # Make sure there is a seed
        if arg_name == "seed" and arg_value is None:
            arg_value = random.randint(1, 10**9)

        # Make the command line arguments names correct
        if arg_name == "view_radius":
            arg_name = "view-radius"
        elif arg_name == "bonus_radius":
            arg_name = "bonus-radius"
        elif arg_name == "torch_delay":
            arg_name = "torch-delay"

        if arg_name == "width" or arg_name == "height":
            command.extend([str(arg_value)])
        else:
            command.extend([f"--{arg_name}", str(arg_value)])

    # Spawn a new process to run the script again, detaching it from the parent process
    subprocess.Popen(command, start_new_session=True)

    # Exit the current process
    sys.exit()


def main():
    """
    Main function where the game is initialised, rendered and the game loop is launched
    :rtype: int
    """

    args = parse_arguments()

    # generate game
    generator = DungeonGenerator(args)
    dungeon_param = generator.generate()

    dungeon = dungeon_param["grid"]
    player = Player(dungeon_param["start_position"], args)
    dungeon_bonuses = dungeon_param["bonuses"]
    dungeon_exit = dungeon_param["exit_position"]

    # render game
    render = Renderer(dungeon, player, dungeon_bonuses, dungeon_exit, args)
    render.show()

    # game_loop
    game_continue = True
    while game_continue:
        direction = input("move your character in the direction you want | w(up),a(left),s(down),d(right):")
        render.move_player(direction)
        render.objects_collapse()
        clear_terminal()
        if render.check_win_loss():
            game_continue = False
        else:
            render.show()

    # relaunch script part
    print("-------------------------------------\n")
    play_again = input("do you want to play again? (Y/N):")

    # check for prompt
    play_again = play_again.upper()
    while play_again != 'Y' and play_again != 'N':
        play_again = input("do you want to play again? (Y/N):")

    if play_again == 'Y':
        clear_terminal()
        modify_param = input("\ndo you want to modify any parameters? (Y/N):")

        # check for prompt
        modify_param = modify_param.upper()
        while modify_param != 'Y' and modify_param != 'N':
            modify_param = input("do you want to modify any parameters? (Y/N):")

        if modify_param == 'Y':
            clear_terminal()
            for arg_name, arg_value in vars(args).items():
                new_value = input(f"Enter a new value for '{arg_name}' (current: {arg_value}) else press enter:")
                if arg_name == "--seed":
                    new_value = int(random.seed)
                if new_value:
                    setattr(args, arg_name, type(arg_value)(new_value))

        # Relaunch the script with the modified arguments
        relaunch_script(args)

    return 0


if __name__ == "__main__":
    main()
