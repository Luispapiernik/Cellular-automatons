import numpy as np

from pycellslib import Automaton, Rule
from pycellslib.cells import StandardCell
from pycellslib.twodimensional.neighborhoods import NeumannNeighborhood
from pycellslib.twodimensional.topologies import FinitePlaneTopology
from pycellslib.visualizers import pygame_visualizer as pv


class FirePropagationRules(Rule):
    """docstring for WireWorldRules"""

    LAND = 0
    TREE = 1
    BURNING_TREE = 2
    BURNED_TREE = 3

    def __init__(self, probability):
        self.probability = probability
        self.neighborhood = NeumannNeighborhood(radius=1, inclusive=True)

    def get_neighborhood(self):
        """
        Este metodo retorna la vecindad asociada a la regla

        Returns
        -------
        out(Neighborhood): Objeto que representa la vecindad
        """
        return self.neighborhood

    def apply_rule(self, cell_states, _):
        """
        Params
        ------
        cell_states(ndarray(int)):

        Returns
        -------
        out(int):
        """
        # indice de la celula del centro
        current_cell = cell_states[cell_states.size // 2]
        # para no contar a la celula del centro se establece el valor a cero
        cell_states[cell_states.size // 2] = 0

        if current_cell == FirePropagationRules.BURNING_TREE:
            return FirePropagationRules.BURNED_TREE, None

        if current_cell == FirePropagationRules.TREE:
            burning_trees = np.sum(
                cell_states[cell_states == FirePropagationRules.BURNING_TREE]
            )

            for i in range(burning_trees):
                if np.random.rand() > self.probability:
                    return FirePropagationRules.BURNING_TREE, None

        return current_cell, None


def fire_propagation():
    dimension = 50
    cell_information = StandardCell(
        [0, 1, 2, 3], name_of_states=["Land", "Tree", "Burning Tree", "Burned Tree"]
    )
    topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
    rule = FirePropagationRules(0.7)

    automaton = Automaton(cell_information, rule, topology, name="Fire Propagation")
    automaton.topology.set_values_from(1, None)

    system = pv.System(
        automaton,
        {
            0: (128, 64, 0),
            1: pv.COLORS["GREEN"],
            2: pv.COLORS["RED"],
            3: pv.COLORS["BLACK"],
        },
    )
    visualizer = pv.CellGraph(
        system,
        margin_width=40,
        margin_height=40,
        background_color=(194, 155, 97),
        cellwidth=10,
        cellheight=10,
        fps=5,
        separation_between_cells=1,
    )

    visualizer.run()


if __name__ == "__main__":
    fire_propagation()
