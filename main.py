from strategies.minmax_strategy import MinmaxStrategy
from strategies.random_strategy import RandomStrategy
from ui.gui import GUI

if __name__ == '__main__':
    # print('\n\n------- GOMOKAI -------')

    # strategy = interface = None
    # while strategy is None:
    #     strategy_choice = input('Difficulty (1 - easy or 2 - hard): ')
    #     if strategy_choice == '1':
    #         strategy = RandomStrategy()
    #     elif strategy_choice == '2':
    #         strategy = MinmaxStrategy()
    strategy = MinmaxStrategy()
    
    interface = GUI(strategy)

    interface.start()
