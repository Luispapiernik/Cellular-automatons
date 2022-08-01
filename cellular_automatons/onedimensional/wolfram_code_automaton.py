from pycellslib import Automaton
from pycellslib.cells import LifeLikeCell
from pycellslib.onedimensional.rules import WolframCodeRule
from pycellslib.onedimensional.topologies import FiniteLineTopology


def show(array):
    string = "|"
    for i in array:
        if i == 0:
            string += " "
        else:
            string += "*"

    return string + "|"


def main():
    cell_information = LifeLikeCell()
    topology = FiniteLineTopology(0, 196, 1)
    rule = WolframCodeRule(90)

    automaton = Automaton(cell_information, rule, topology)

    automaton.topology.update_cell((0, 100), 1, None)

    for _ in range(100):
        string = show(automaton.topology.get_states()[0])
        print(string)

        automaton.next_step()


if __name__ == "__main__":
    main()
