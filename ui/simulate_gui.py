import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN
from strategies.strategy import Strategy
from strategies.random_strategy import RandomStrategy
from constants import Player,getEnemy
from game import Game
from ui.renderer import GameRenderer
from typing import Tuple
import time
import threading
class SimulateGUI:
    def __init__(self, strategy1:Strategy,strategy2:Strategy):
        self.strategy1=strategy1
        self.strategy2=strategy2
        self._game = Game()
        self._renderer = GameRenderer(self._game)
        self.state:Player=Player.NONE
        self.move:None|Tuple[int,int]=None
        # self.clock = pygame.time.Clock()

    def start_game(self):
        self._renderer.draw_board()
        self._game.restart()
        self.move=self._game.computer_move(Player.BLACK,RandomStrategy())
        # self._renderer.place_piece_at_cell(_r, _c, Player.BLACK)
        self.state=Player.BLACK

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
    def get_npc_move(self,player:Player,strategy:Strategy):
        move= self._game.computer_move(player,strategy)
        if move[0]==-1 or move[1]==-1:
            self.move=None
        else:
            self.move=move
    def start(self):
        self.start_game()
        loading_count=0
        # Main loop
        while True:
            
            try:
                # self.clock.tick(60)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if self._renderer.was_play_again_pressed() and self.state==Player.NONE:
                                self.start_game()
                if not self._game.is_game_finished and self.state==Player.BLACK:
                    if self.move is not None:
                        row,column=self.move
                        self._renderer.place_piece_at_cell(row, column, Player.BLACK)
                        self.move=None
                        self.state=Player.WHITE
                        threading.Thread(target=self.get_npc_move, args=[Player.WHITE,self.strategy2]).start()
                    self._renderer.draw_message('Waiting for player black')

                if not self._game.is_game_finished and self.state==Player.WHITE:
                    if self.move is not None:
                        row,column=self.move
                        self._renderer.place_piece_at_cell(row, column, Player.WHITE)
                        self.move=None
                        self.state=Player.BLACK
                        threading.Thread(target=self.get_npc_move, args=[Player.BLACK,self.strategy1]).start()
                    self._renderer.draw_message('Waiting for player white')

                if self._game.is_game_finished and not self.state==Player.NONE:
                    self.draw_winner()
                    self.state = Player.NONE
                pygame.display.update()
            except ValueError as exception:
                print(exception)
