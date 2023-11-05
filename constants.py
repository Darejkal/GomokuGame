from enum import Enum
import typing

BOARD_SIZE = 15

WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#222222"

row_change = [-1, -1, 0, 1, 1, 1, 0, -1]
col_change = [0, 1, 1, 1, 0, -1, -1, -1]


class Player(Enum):
    NONE = ' '
    BLACK = 'B'
    WHITE = 'W'
def getEnemy(value:Player):
    if(value==Player.BLACK):
        return Player.WHITE
    if(value==Player.WHITE):
        return Player.BLACK
    return Player.NONE
