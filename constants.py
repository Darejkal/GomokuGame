from enum import Enum
import typing
INF = int(7e12)
BOARD_SIZE = 15

WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#222222"

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
