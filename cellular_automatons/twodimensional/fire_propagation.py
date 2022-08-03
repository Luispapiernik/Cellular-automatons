import matplotlib.cm as cm
import numpy as np
from pycellslib import Automaton, Rule
from pycellslib.cells import StandardCell
from pycellslib.twodimensional.neighborhoods import NeumannNeighborhood
from pycellslib.twodimensional.topologies import FinitePlaneTopology
from pycellslib.visualizers import pygame_visualizer as pv
from scipy.stats import truncnorm


class FirePropagationDiscreteRule(Rule):
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

        if current_cell == FirePropagationDiscreteRule.BURNING_TREE:
            return FirePropagationDiscreteRule.BURNED_TREE, None

        if current_cell == FirePropagationDiscreteRule.TREE:
            burning_trees = np.sum(
                cell_states[cell_states == FirePropagationDiscreteRule.BURNING_TREE]
            )

            for i in range(burning_trees):
                if np.random.rand() > self.probability:
                    return FirePropagationDiscreteRule.BURNING_TREE, None

        return current_cell, None


class DiscreteFirePropagation:
    def __init__(self, dimension: int = 50) -> None:
        cell_information = StandardCell(
            [0, 1, 2, 3], name_of_states=["Land", "Tree", "Burning Tree", "Burned Tree"]
        )
        topology = FinitePlaneTopology(0, dimension, dimension, 3, 3)
        rule = FirePropagationDiscreteRule(0.7)

        self.automaton = Automaton(
            cell_information, rule, topology, name="Fire Propagation"
        )

    def iterate(self):
        self.automaton.topology.set_values_from(1, None)
        system = pv.System(
            self.automaton,
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


class AumentedCell(StandardCell):
    """docstring for AumentedCell"""

    def __init__(self, burning_states_number):
        super().__init__(burning_states_number + 1)

    def get_number_of_attributes(self):
        """
        Este metodo retorna el numero de atributos que tiene una celula. En
        caso de que la celula no tenga atributos se retorna 0

        Returns
        -------
        out(int): numero de atributos de una celula
        """
        return 1

    def get_default_value_of_attributes(self):
        """
        Este metodo retorna los valores que tiene una celula por defecto en
        cada atributo. En caso de que la celula no tenga atributos, se retorna
        None

        Returns
        -------
        out(None): valores por defecto de los atributos de la celula.
        """
        return 0

    # con el objetivo de obtener y mostrar informacion del automata, como
    # densidad, flujos, ... se nombran los atributos, los cuales tienen un
    # orden fijo
    def get_name_of_attributes(self, index):
        """
        Este metodo retorna el nombre del atributo asociado a un indice, el
        indice cuenta desde cero. Se retorna None en caso de que la celula no
        tenga atributos

        Params
        ------
        index(int): indice que corresponde al atributo

        Returns
        -------
        out(None): nombre del atributo, puede ser un string vacio
        """
        return "Age"


class FirePropagationRule(Rule):
    """docstring for WireWorldRules"""

    def __init__(self, probability, burning_states_number=1):
        self.max_probability = probability
        self.neighborhood = NeumannNeighborhood(radius=1, inclusive=True)

        self.burned_state = 2 + burning_states_number
        # parametros para la distribucion normal truncada
        self.a = 2
        self.b = self.burned_state

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

        # si es un arbol no quemado
        if current_cell == 1:
            inf_limit = 1 < cell_states
            sup_limit = cell_states < self.burned_state
            burning_trees = np.sum(cell_states[inf_limit & sup_limit])

            for i in range(burning_trees):
                if np.random.rand() > self.max_probability - truncnorm.pdf(
                    current_cell, self.a, self.b
                ):
                    return 2, None

        # si se esta quemando
        if 1 < current_cell < self.burned_state:
            return current_cell + 1, None

        return current_cell, None


class FirePropagation:
    def __init__(self, dimension: int = 70, burning_states_number: int = 30) -> None:
        self.burning_states_number = burning_states_number
        cell_information = AumentedCell(burning_states_number)
        topology = FinitePlaneTopology(1, dimension, dimension, 3, 3)
        rule = FirePropagationRule(0.7, burning_states_number)

        self.automaton = Automaton(
            cell_information, rule, topology, name="Fire Propagation"
        )

    def get_colors(self, burning_states_number):
        states_number = burning_states_number + 2 + 1
        colors = {0: (128, 64, 0), 1: pv.COLORS["GREEN"]}

        last_level = 0.8
        diff = last_level / (burning_states_number - 1)
        for i in range(2, states_number):
            colors[i] = tuple(int(255 * i) for i in cm.hot(last_level - diff * (i - 2)))

        return colors

    def iterate(self):
        self.automaton.topology.set_values_from(1, None)

        system = pv.System(self.automaton, self.get_colors(self.burning_states_number))
        visualizer = pv.CellGraph(
            system,
            margin_width=40,
            margin_height=40,
            background_color=(194, 155, 97),
            cellwidth=10,
            cellheight=10,
            fps=5,
            separation_between_cells=0,
        )

        visualizer.run()
