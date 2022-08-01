import numpy as np

from pycellslib import Automaton
from pycellslib.cells import LifeLikeCell
from pycellslib.twodimensional.rules import BSNotationRule
from pycellslib.twodimensional.topologies import FinitePlaneTopology
from pycellslib.visualizers import matplotlib_visualizer as mv


def get_random_configuration(dimension):
    """returns a grid of (dimension, dimension) random values"""
    configuration = np.random.choice([0, 1], dimension * dimension)
    return configuration.reshape(dimension, dimension)


def main():
    dimension = 30
    cell_information = LifeLikeCell()
    topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
    rule = BSNotationRule([3], [2, 3], radius=1)

    automaton = Automaton(cell_information, rule, topology)
    automaton.topology.set_values_from_configuration(
        get_random_configuration(dimension), None
    )

    fig, axes = mv.configure_animation("Game Of Life")
    animation = mv.animate(
        automaton, fig, axes, frames=1000, time_per_frame=50, save_count=None
    )

    animation.save("prueba.mp4")


if __name__ == "__main__":
    main()
