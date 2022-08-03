from pycellslib import Automaton
from pycellslib.cells import LifeLikeCell
from pycellslib.onedimensional.rules import WolframCodeRule
from pycellslib.onedimensional.topologies import FiniteLineTopology


class WolframCodeAutomaton:
    def __init__(self, width: int = 180, wolfram_rule: int = 90) -> None:
        cell_information = LifeLikeCell()
        topology = FiniteLineTopology(0, width, 1)
        rule = WolframCodeRule(wolfram_rule)

        self.automaton = Automaton(cell_information, rule, topology)

    def show(self, array) -> str:
        string = "|"
        for i in array:
            if i == 0:
                string += " "
            else:
                string += "*"

        return string + "|"

    def set_cell_value(self, cell_index: int, value: int) -> None:
        self.automaton.topology.update_cell((0, cell_index), value, None)

    def iterate(self, iterations: int) -> None:
        for _ in range(iterations):
            string = self.show(self.automaton.topology.get_states()[0])
            print(string)

            self.automaton.next_step()
