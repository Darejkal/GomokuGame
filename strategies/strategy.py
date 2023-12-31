from abc import ABC, abstractmethod
from board import Board
from constants import Player
from typing import Tuple
class Strategy(ABC):
    """
    Abstract class that should be implemented by strategies
    """
    @abstractmethod
    def make_move(self, board:Board, player_colour:Player) -> Tuple[int,int]:
        """
        This should apply a move to the board and also return the move made, that is a tuple of two integers
        :param board: Board object
        :param player_colour: player at move
        :return: tuple of two integers
        """
        pass
