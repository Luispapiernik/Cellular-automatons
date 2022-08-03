import numpy as np
from pycellslib import Automaton
from pycellslib.cells import LifeLikeCell
from pycellslib.twodimensional.rules import BSNotationRule
from pycellslib.twodimensional.topologies import FinitePlaneTopology
from pycellslib.visualizers import matplotlib_visualizer as mv
from pycellslib.visualizers import pygame_visualizer as pv


class GameOfLifeMatplotlib:
    def __init__(self, dimension: int = 30) -> None:
        self.dimension = dimension

        cell_information = LifeLikeCell()
        topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
        rule = BSNotationRule([3], [2, 3], radius=1)

        self.automaton = Automaton(cell_information, rule, topology)

    def get_random_configuration(self, dimension: int):
        """returns a grid of (dimension, dimension) random values"""
        configuration = np.random.choice([0, 1], dimension * dimension)
        return configuration.reshape(dimension, dimension)

    def iterate(self, iterations: int) -> None:
        self.automaton.topology.set_values_from_configuration(
            self.get_random_configuration(self.dimension), None
        )

        fig, axes = mv.configure_animation("Game Of Life")
        animation = mv.animate(
            self.automaton,
            fig,
            axes,
            frames=iterations,
            time_per_frame=50,
            save_count=None,
        )

        animation.save(f"game_of_life_{self.dimension}_{iterations}.mp4")


class GameOfLifePygame:
    def __init__(self, dimension: int = 50) -> None:
        self.dimension = dimension
        cell_information = LifeLikeCell()
        topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
        rule = BSNotationRule([3], [2, 3], radius=1)

        self.automaton = Automaton(
            cell_information, rule, topology, name="Game Of Life"
        )

    def iterate(self):
        self.automaton.topology.set_values_from_configuration(
            self.get_random_configuration(self.dimension), None
        )

        system = pv.System(
            self.automaton, {0: pv.COLORS["WHITE"], 1: pv.COLORS["BLACK"]}
        )
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

    def get_random_configuration(self, dimension):
        """returns a grid of (dimension, dimension) random values"""
        configuration = np.random.choice([0, 1], dimension * dimension)
        return configuration.reshape(dimension, dimension)
