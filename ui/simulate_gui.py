import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN
from strategies.strategy import Strategy
from strategies.random_strategy import RandomStrategy
from constants import Player,getEnemy
from strategies.strategy import Strategy
from strategies.minmax_strategy import MinmaxStrategy
from strategies.genetic_strategy import GeneticStrategy
from game import Game
from ui.renderer import GameRenderer
from typing import Tuple
import time
import threading
def getStrategyStr(strategy:Strategy):
    if isinstance(strategy,MinmaxStrategy):
        return f"MinMax-{strategy.depth}"
    elif isinstance(strategy,GeneticStrategy):
        return "Genetic"
    return "UnknownStrategy"
class SimulateGUI:
    def __init__(self, strategy1:Strategy,strategy2:Strategy):
        self.strategy1=strategy1
        self.strategy2=strategy2
        self._game = Game()
        self._renderer = GameRenderer(self._game)
        self.state:Player=Player.NONE
        self.move:None|Tuple[int,int]=None
        self.turn_count=1
        # self.clock = pygame.time.Clock()

    def start_game(self):
        self.turn_count=1
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
                if  self.state==Player.BLACK:
                    if self.move is not None:
                        row,column=self.move
                        self._renderer.place_piece_at_cell(row, column, Player.BLACK)
                        self._renderer.draw_text_at_cell(row,column,str(self.turn_count))
                        self.turn_count+=1
                        if not self._game.is_game_finished:
                            self.move=None
                            self.state=Player.WHITE
                            threading.Thread(target=self.get_npc_move, args=[Player.WHITE,self.strategy2]).start()
                        else:
                            self.move=(-1,-1)
                    self._renderer.draw_message('Waiting for player black')

                if self.state==Player.WHITE:
                    if self.move is not None:
                        row,column=self.move
                        self._renderer.place_piece_at_cell(row, column, Player.WHITE)
                        self._renderer.draw_text_at_cell(row,column,str(self.turn_count))
                        self.turn_count+=1
                        if not self._game.is_game_finished:
                            self.move=None
                            self.state=Player.BLACK
                            threading.Thread(target=self.get_npc_move, args=[Player.BLACK,self.strategy1]).start()
                        else:
                            self.move=(-1,-1)
                    self._renderer.draw_message('Waiting for player white')

                if self._game.is_game_finished and self.move is (-1,-1) and not self.state==Player.NONE:
                    with open("data.txt","a+") as f:
                        winner=self.strategy1 if self.state==Player.BLACK else self.strategy2
                        loser=self.strategy2 if self.state==Player.BLACK else self.strategy1
                        f.write(f"{getStrategyStr(winner)} {'draws' if self._game.board.is_draw else 'win'} {getStrategyStr(loser)} {self.turn_count}\n")
                    self.move=(-1,-1)
                    self.draw_winner()
                    self.state = Player.NONE
                    # to remove
                    self.start_game()
                pygame.display.update()
            except ValueError as exception:
                print(exception)
