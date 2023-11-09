from strategies.minmax_strategy import MinmaxStrategy
from strategies.genetic_strategy import GeneticStrategy
from strategies.random_strategy import RandomStrategy
from ui.gui import GUI
from ui.simulate_gui import SimulateGUI

if __name__ == '__main__':
    interface = GUI(MinmaxStrategy())
    # interface = SimulateGUI(GeneticStrategy(),MinmaxStrategy())

    interface.start()
