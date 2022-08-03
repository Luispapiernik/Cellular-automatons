import numpy as np
from pycellslib import Automaton, Rule
from pycellslib.cells import StandardCell
from pycellslib.twodimensional.neighborhoods import MooreNeighborhood
from pycellslib.twodimensional.topologies import FinitePlaneTopology
from pycellslib.visualizers import pygame_visualizer as pv


class WireWorldRules(Rule):
    """docstring for WireWorldRules"""

    EMPTY = 0
    ELECTRON_HEAD = 1
    ELECTRON_TAIL = 2
    CONDUCTOR = 3

    def __init__(self):
        self.neighborhood = MooreNeighborhood(radius=1, inclusive=True)

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

        if current_cell == WireWorldRules.ELECTRON_HEAD:
            return WireWorldRules.ELECTRON_TAIL, None
        if current_cell == WireWorldRules.ELECTRON_TAIL:
            return WireWorldRules.CONDUCTOR, None
        if current_cell == WireWorldRules.CONDUCTOR:
            electron_heads = np.sum(
                cell_states[cell_states == WireWorldRules.ELECTRON_HEAD]
            )
            if electron_heads in [1, 2]:
                return WireWorldRules.ELECTRON_HEAD, None

            return WireWorldRules.CONDUCTOR, None

        return 0, None


class WireWorld:
    def __init__(self, dimension: int = 25) -> None:
        cell_information = StandardCell(
            [0, 1, 2, 3],
            name_of_states=["Empty", "Electron Head", "Electron Tail", "Conductor"],
        )
        topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
        rule = WireWorldRules()

        self.automaton = Automaton(cell_information, rule, topology, name="Wire World")

    def iterate(self):
        system = pv.System(
            self.automaton,
            {
                0: pv.COLORS["BLACK"],
                1: pv.COLORS["BLUE"],
                2: pv.COLORS["RED"],
                3: pv.COLORS["YELLOW"],
            },
        )
        visualizer = pv.CellGraph(
            system,
            margin_width=40,
            margin_height=40,
            background_color=(155, 155, 155),
            cellwidth=20,
            cellheight=20,
            fps=5,
            separation_between_cells=1,
        )

        visualizer.run()
