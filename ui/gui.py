import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN
from strategies.strategy import Strategy
from constants import Player
from game import Game
from ui.renderer import GameRenderer


class GUI:
    def __init__(self, strategy:Strategy):
        self.strategy=strategy
        self._game = Game()
        self._renderer = GameRenderer(self._game)
        self._waiting_for_restart = False

    def start_game(self):
        self._renderer.draw_board()
        self._game.restart()
        self._waiting_for_restart = False
        self._renderer.draw_message('You start! (Black)')

    def draw_winner(self):
        if self._game.board.board_winner == Player.WHITE:
            self._renderer.draw_message('White player won', game_over=True)
            print('White won the game!')
        elif self._game.board.board_winner == Player.BLACK:
            self._renderer.draw_message('Black player won', game_over=True)
            print('Black won the game!')
        else:
            self._renderer.draw_message('Draw', game_over=True)
            print('Draw!')

    def start(self):
        self.start_game()
        preRow,preColumn=None,None
        # Main loop
        while True:
            try:
                for event in pygame.event.get():

                    if event.type == QUIT:
                        exit()

                    elif event.type == MOUSEBUTTONDOWN:
                        # In case something was pressed
                        position = pygame.mouse.get_pos()

                        if self._game.is_game_finished:
                            if self._renderer.was_play_again_pressed():
                                self.start_game()
                        else:
                            (row, column) = self._renderer.coordinate_transform_pixel2map(*position)
                            if row is not -1 and column is not -1:
                                self._game.human_move(row, column, Player.BLACK)
                                self._renderer.place_piece_at_cell(row, column, Player.BLACK)

                                if not self._game.is_game_finished:
                                    # Computer step
                                    self._renderer.draw_message('Waiting for computer')
                                    pygame.display.update()
                                    row, column = self._game.computer_move(Player.WHITE,self.strategy)
                                    if row is not -1 and column is not -1:
                                        self._renderer.place_piece_at_cell(row, column, Player.WHITE)
                                        self._renderer.draw_message('Your turn')

                if self._game.is_game_finished and not self._waiting_for_restart:
                    self.draw_winner()
                    self._waiting_for_restart = True
                position = pygame.mouse.get_pos()
                (row, column) = self._renderer.coordinate_transform_pixel2map(*position)
                if preRow is not None and preColumn is not None:
                    self._renderer.highlight_at_cell(preRow,preColumn,False,self._game.board.get_cell_value(preRow,preColumn))
                if row is not None and column is not None:
                    self._renderer.highlight_at_cell(row,column,True,self._game.board.get_cell_value(row,column))
                    preRow,preColumn=row,column
                # update
                pygame.display.update()
            except ValueError as exception:
                print(exception)
