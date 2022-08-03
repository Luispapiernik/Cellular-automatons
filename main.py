from argparse import ArgumentParser

from cellular_automatons.onedimensional import WolframCodeAutomaton
from cellular_automatons.twodimensional import (
    DiscreteFirePropagation,
    FirePropagation,
    GameOfLifeMatplotlib,
    GameOfLifePygame,
    WireWorld,
)


def execute(args):
    if args.wolfram_automaton:
        wolfram_automaton = WolframCodeAutomaton()
        wolfram_automaton.set_cell_value(100, 1)
        wolfram_automaton.iterate(100)

    if args.game_of_life_matplotlib:
        game_of_life_matplotlib = GameOfLifeMatplotlib()
        game_of_life_matplotlib.iterate(100)

    if args.game_of_life_pygame:
        game_of_life_pygame = GameOfLifePygame()
        game_of_life_pygame.iterate()

    if args.discrete_fire_propagation:
        discrete_fire_propagation = DiscreteFirePropagation()
        discrete_fire_propagation.iterate()

    if args.fire_propagation:
        fire_propagation = FirePropagation(70, 45)
        fire_propagation.iterate()

    if args.wire_world:
        wire_world = WireWorld()
        wire_world.iterate()


def main():
    parser = ArgumentParser()
    parser.add_argument("-wa", "--wolfram-automaton", action="store_true")
    parser.add_argument("-glm", "--game-of-life-matplotlib", action="store_true")
    parser.add_argument("-glp", "--game-of-life-pygame", action="store_true")
    parser.add_argument("-dfp", "--discrete-fire-propagation", action="store_true")
    parser.add_argument("-fp", "--fire-propagation", action="store_true")
    parser.add_argument("-w", "--wire-world", action="store_true")

    args = parser.parse_args()
    execute(args)


if __name__ == "__main__":
    main()
