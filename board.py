from constants import Player, row_change, col_change,getEnemy
from typing import Literal,List,Tuple
import random
class Board:
    """
    Class that manages the Gomoku board
    """

    def __init__(self, board_size:int, previous_data:None|list[list[Player]]=None):
        """
        Initializes the Gomoku Board
        :param board_size: integer
        :param previous_data: if the board is a duplicate of another board, this is a matrix
                              with previous board data. This is copied to prevent shallow copy problems
        """
        self._board_size:int = board_size
        self._board_winner:Player = Player.NONE
        self._last_move_line:int|None = None
        self._last_move_column:int|None = None
        self._number_of_empty_cells = board_size * board_size

        if previous_data is not None:
            self._data = [[previous_data[row][col] for col in range(board_size)] for row in range(board_size)]
        else:
            self._data = [[Player.NONE for j in range(self._board_size)] for i in range(self._board_size)]

    @property
    def board_size(self):
        return self._board_size
    @property
    def board_height(self):
        return self._board_size
    @property
    def board_width(self):
        return self._board_size

    @property
    def board_winner(self):
        return self._board_winner

    @property
    def last_move(self):
        return self._last_move_line, self._last_move_column

    @property
    def is_draw(self):
        return self._number_of_empty_cells == 0

    @property
    def data(self):
        return self._data

    def get_new_board_apply(self,player:Player,moves:List[Tuple[int,int]]):
        r=Board(self.board_size,self.data[:])
        flag=True
        for m in moves:
            if flag:
                r.set(m[0],m[1],player)
            else:
                r.set(m[0],m[1],getEnemy(player))
            flag=not flag
        return r

    def get_cell_value(self, row:int, column:int)->Player:
        """
        Gets the value at row and column
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :return: Player.NONE or Player.WHITE or Player.BLACK
        """
        return self._data[row][column]

    def is_cell_empty(self, row:int, column:int)->bool:
        """
        Checks if cell at row and column is empty
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :return: True if value is NONE and False if value is not NONE
        """
        return self.get_cell_value(row, column) == Player.NONE

    def get_filled_cells(self)->List[Tuple[int,int]]:
        """
        Returns a list of tuples (row,column) that already have a piece placed
        :return: list of two integer tuples
        """
        return [(row, column) for column in range(self.board_size) for row in range(self.board_size) if
                not self.is_cell_empty(row, column)]

    def set(self, row:int, column:int, player_colour:Player):
        """
        Places a piece at (row, column) and then updates the board status.
        Checks if the piece made someone a winner
        :param row: integer in range [0, board size]
        :param column: integer in range [0, board size]
        :param player_colour: Player.WHITE or Player.BLACK
        """
        self._data[row][column] = player_colour
        self._number_of_empty_cells -= 1
        self._last_move_line, self._last_move_column = row, column
        self._check_for_winner()

    def set_without_checking(self, row:int, column:int, player_colour:Player):
        """
        Places a piece at (row, column) but does not check if it made someone a winner
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :param player_colour: Player.WHITE or Player.BLACK
        :return: None
        """
        self._data[row][column] = player_colour
    def set_silently(self, row:int, column:int, player_colour:Player):
        """
        Places a piece at (row, column) 
        but does not broadcast to the board if the action made someone a winner
        and returns a flag instead
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :param player_colour: Player.WHITE or Player.BLACK
        :return: true if there is a winner after the action, false otherwise
        """
        self._data[row][column] = player_colour
        for direction in range(4):
            line = self.get_line_of_characters(row, column, direction, must_be_the_same=True)
            if Player.WHITE.value * 5 in line:
                return True
            elif Player.BLACK.value * 5 in line:
                return True
        return False

    def are_coordinates_valid(self, row:int, column:int)->bool:
        """
        Checks if row and column are in the valid range
        :param row: integer
        :param column: integer
        :return: True if coordinates are valid and False otherwise
        """
        return 0 <= row < self.board_size and 0 <= column < self._board_size

    def _check_for_winner(self):
        """
        Checks if there is a winner in the current board placement.
        If there is a winner, it is marked in the "self._board_winner" attribute of the board.
        """
        if self._last_move_line==None or self._last_move_column==None:
            return
        for direction in range(4):
            row, column = self._last_move_line, self._last_move_column
            line = self.get_line_of_characters(row, column, direction, must_be_the_same=True)
            if Player.WHITE.value * 5 in line:
                self._board_winner = Player.WHITE
            elif Player.BLACK.value * 5 in line:
                self._board_winner = Player.BLACK


    def get_line_of_characters(self, row:int, col:int, direction:int, must_be_the_same:bool=False)->str:
        """
        From a given cell, gets row/column/diagonal in the direction specified
        Beginning from the cell, it expands at most 7 cells in both directions
        If must_be_the_same is True, it only expands if the next cells are the same with the given cell
        :param row: integer in range [0, board size-1]
        :param col: integer in range [0, board size-1]
        :param direction: integer in range [0, 7], 0 being north and going clockwise
        :param must_be_the_same: optional boolean character
        :return: string with characters ' ', 'B' and 'W'
        """
        cell_value = self.get_cell_value(row, col)
        line = cell_value.value

        new_row, new_col = row, col
        length:int = 0

        while self.are_coordinates_valid(new_row + row_change[direction], new_col + col_change[direction]) \
                and length < 7:

            if must_be_the_same and self.get_cell_value(new_row + row_change[direction],
                                                        new_col + col_change[direction]) != cell_value:
                break

            length += 1
            new_row += row_change[direction]
            new_col += col_change[direction]
            line = line + self.get_cell_value(new_row, new_col).value

        new_row, new_col = row, col
        length = 0

        while self.are_coordinates_valid(new_row - row_change[direction], new_col - col_change[direction]) \
                and length < 7:

            if must_be_the_same and self.get_cell_value(new_row - row_change[direction],
                                                        new_col - col_change[direction]) != cell_value:
                break

            length += 1
            new_row -= row_change[direction]
            new_col -= col_change[direction]
            line = self.get_cell_value(new_row, new_col).value + line

        return line
    def getRandomCell(self):
        return (random.randint(1,self.board_size),random.randint(1,self.board_size))
    # @staticmethod
    # def cell_to_character(value):
    #     """
    #     Converts Player value to one character
    #     :param value: Player.BLACK, Player.NONE or Player.WHITE
    #     :return: 'B', ' ' or 'W'
    #     """
    #     if value == Player.BLACK:
    #         return 'B'
    #     elif value == Player.WHITE:
    #         return 'W'
    #     else:
    #         return ' '
