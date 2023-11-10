from enum import Enum
import typing
INF = int(7e12)
BOARD_SIZE = 10

WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#222222"
# Scores used to evaluate a given board, + being a piece of the player at move and - the other player
HEURISTIC_SCORES = {
    "-----": -2000000000000,
    "+++++": 1000000000000,
    " ---- ": -50000000000,
    " ++++ ": 10000000000,
    "-++++ ": 100000000,
    " ++++-": 100000000,
    " ----+": -500000000,
    "+---- ": -500000000,
    " +++ ": 1000,
    " +++-": 150,
    " ---+": -50,
    " --- ": -5000,
    " ++ ": 10,
    " -- ": -50
}
HEURISTIC_SCORES_GENETICS = {
    "-----": -2000000000000,
    "+++++": 1000000000000,
    " ---- ": -50000000000,
    " ++++ ": 10000000000,
    "-++++ ": 100000000,
    " ++++-": 100000000,
    " ----+": -500000000,
    "+---- ": -500000000,
    " +++ ": 1000,
    " +++-": 150,
    " ---+": -50,
    " --- ": -5000,
    " ++ ": 10,
    " -- ": -50
}
row_change = [-1, -1, 0, 1, 1, 1, 0, -1]
col_change = [0, 1, 1, 1, 0, -1, -1, -1]

class OrderedEnum(Enum):
    def __ge__(self, other):

        if self.__class__ is other.__class__:

            return self.value >= other.value

        return NotImplemented
    def __gt__(self, other):

        if self.__class__ is other.__class__:

            return self.value > other.value

        return NotImplemented
    def __le__(self, other):

        if self.__class__ is other.__class__:

            return self.value <= other.value

        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:

            return self.value < other.value
        return NotImplemented
class Player(OrderedEnum):
    NONE = ' '
    BLACK = 'B'
    WHITE = 'W'

def getEnemy(value:Player):
    if(value==Player.BLACK):
        return Player.WHITE
    if(value==Player.WHITE):
        return Player.BLACK
    return Player.NONE
