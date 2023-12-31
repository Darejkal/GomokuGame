from board import Board
from constants import BOARD_SIZE, Player
from strategies.strategy import Strategy
from strategies.minmax_strategy import MinmaxStrategy
from strategies.genetic_strategy import GeneticStrategy
import time
class Game:
    """
    Class that manages the game actions
    """
    def __init__(self):
        """
        Initializes the game
        :param strategy: class that implements Strategy abstract class
        """
        self._board = Board(BOARD_SIZE)

    def restart(self):
        """
        Makes a new empty board
        """
        self._board = Board(BOARD_SIZE)

    def human_move(self, line, column, player_colour):
        """
        Checks if the user choice is valid and applies it to the board
        :param line: integer from 0 to board size - 1
        :param column: integer from 0 to board size - 1
        :param player_colour: Player.WHITE or Player.BLACK
        Raises ValueError if line or column ar not in valid range
        Raises ValueError if the cell is not empty
        """
        if not 0 <= line < self.board.board_size:
            raise ValueError('Line value out of range!')

        if not 0 <= column < self.board.board_size:
            raise ValueError('Column value out of range!')

        if not self.board.is_cell_empty(line, column):
            raise ValueError('Cell not empty!')
        self.board.set(line, column, player_colour)
        print(f"{'Black' if player_colour==Player.BLACK else 'White'} played",(line,column))

    def computer_move(self, player_colour:Player,strategy:Strategy):
        """
        Calls the strategy to compute the next move and returns it to be displayed
        :param player_colour: Player.BLACK or Player.WHITE, the player of the computer
        :return: a tuple (row,column), the coordinates of the move played by the computer
        """
        begin_time = time.time()
        move= strategy.make_move(self.board, player_colour)
        print(f"{'Black' if player_colour==Player.BLACK else 'White'} played",move)
        self._board.set(move[0],move[1],player_colour)
        run_diff=(time.time()-begin_time)
        print("-> Time:%.3f"%run_diff)
        return move

    @property
    def board(self):
        return self._board

    @property
    def is_game_finished(self):
        """
        Getter, indicates if the games is over
        :return: boolean value
        """
        return self._board.board_winner != Player.NONE or self._board.is_draw
