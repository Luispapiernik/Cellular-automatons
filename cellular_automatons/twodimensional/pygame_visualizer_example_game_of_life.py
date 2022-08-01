import numpy as np

from pycellslib import Automaton
from pycellslib.cells import LifeLikeCell
from pycellslib.twodimensional.rules import BSNotationRule
from pycellslib.twodimensional.topologies import FinitePlaneTopology
from pycellslib.visualizers import pygame_visualizer as pv


def get_random_configuration(dimension):
    """returns a grid of (dimension, dimension) random values"""
    configuration = np.random.choice([0, 1], dimension * dimension)
    return configuration.reshape(dimension, dimension)


def game_of_life():
    dimension = 50
    cell_information = LifeLikeCell()
    topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
    rule = BSNotationRule([3], [2, 3], radius=1)

    automaton = Automaton(cell_information, rule, topology, name="Game Of Life")
    automaton.topology.set_values_from_configuration(
        get_random_configuration(dimension), None
    )

    system = pv.System(automaton, {0: pv.COLORS["WHITE"], 1: pv.COLORS["BLACK"]})
    visualizer = pv.CellGraph(
        system,
        margin_width=40,
        margin_height=40,
        background_color=(0, 0, 0),
        cellwidth=10,
        cellheight=10,
        fps=5,
        separation_between_cells=1,
    )

    visualizer.run()


if __name__ == "__main__":
    game_of_life()
