import random
from typing import Tuple
import constants
from strategies.strategy import Strategy
from board import Board
from constants import Player

class RandomStrategy(Strategy):
    """
    Random strategy
    """
    def make_move(self, board:Board, player_colour:Player)->Tuple[int,int]:
        """
        Computes a valid move around last placed piece randomly.
        If it is not possible, places at any valid cell.
        :param board: Board object
        :param player_colour: Player.WHITE or Player.BLACK
        :return: tuple of two integers
        """
        last_line, last_column = board.last_move
        if last_line==None or last_column==None:
            last_line,last_column=board.getRandomCell()
        for direction in random.sample(range(8), k=8):
            move_line = last_line + constants.row_change[direction]
            move_column = last_column + constants.col_change[direction]

            if board.are_coordinates_valid(move_line, move_column) \
                    and board.is_cell_empty(move_line, move_column):
                board.set(move_line, move_column, player_colour)
                return move_line, move_column

        for line in range(board.board_size):
            for column in range(board.board_size):
                if board.is_cell_empty(line, column):
                    board.set(line, column, player_colour)
                    return line, column

        return -1,-1
