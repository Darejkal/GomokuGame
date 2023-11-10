import copy
import random
from collections import Counter
import time
from typing import Tuple, List,Callable,TypeVar, Generic
from board import Board
from strategies.strategy import Strategy
from strategies.minmax_strategy import MinmaxStrategy
from constants import Player,getEnemy,INF,HEURISTIC_SCORES_GENETICS
# def evaluate_cell_and_get_winning_flag(board:Board, row:int, column:int):
#     """
#     Heuristic that computes the importance of a given piece on the board,
#     depending on the length of the same colour piece line it forms
#     :param board: Board object
#     :param row: integer in range [0, board size - 1]
#     :param column: integer in range [0, board size - 1]
#     :return: Integer value denoting the importance and a flag on whether someone will win if a move on the cell is made in the next turn
#     """
#     if board.get_cell_value(row, column) != Player.NONE:
#         return 0,False
#     value = 0

#     flag=board.set_silently(row, column, Player.WHITE)
#     for direction in range(4):
#         value += (len(board.get_line_of_characters(row, column, direction, must_be_the_same=True))-1) * 500
#     flag= flag or board.set_silently(row, column, Player.BLACK)
#     for direction in range(4):
#         value += (len(board.get_line_of_characters(row, column, direction, must_be_the_same=True))-1) * 500
#     board.set_without_checking(row, column, Player.NONE)
#     return value,flag
def evaluate_board(board:Board, player:Player, moves_so_far:List[Tuple[int,int]])->int:
    """
    Heuristic function to evaluate the entire board.
    :param board: Board object
    :param player: Player.WHITE or Player.BLACK, maximizer player
    :param moves_so_far: list of (row,column), representing cells already placed in the recursion tree
    :return: The score of the whole board, after evaluation
    """
    score = 0
    maximizer = player
    minimizer = getEnemy(player)

    for row, column in moves_so_far:
        for direction in range(4):
            line = board.get_line_of_characters(row, column, direction)
            line = line.replace(maximizer.value, '+').replace(minimizer.value, '-')

            values = {}
            substrings = [line[i:i + length] for length in [4, 5, 6] for i in range(len(line)) if
                            i + length < len(line)]
            for substring in substrings:
                values[substring] = values[substring] + 1 if substring in values else 1

            for item in HEURISTIC_SCORES_GENETICS.keys():
                score += HEURISTIC_SCORES_GENETICS[item] * values[item] if item in values else 0
    return score
# def eval_individual(board:Board, player:Player,opponent:Player,moves:List[Tuple[int,int]],n_in_line = 5):
#     if len(set(moves)) != len(moves):
#         return -1
#     current_board = Board(board.board_size,board.data[:])
#     value = 0
#     sign = 1
#     players=[player,opponent]
#     me_win = False
#     opp_win = False 
#     for move in moves:
#         if me_win:
#             value += 2 * 100000
#         elif opp_win:
#             value -= 2 * 100000
#         else:
#             evaluation = evaluate_cell_and_get_winning_flag(current_board,*move)
#             if evaluation[1]:
#                 if players[0] == evaluation[1]: 
#                     me_win = True
#                 else: 
#                     opp_win = True
#             value += sign * evaluation[0]
#             current_board.set(move[0],move[1],players[0])
#             sign = -sign
#             players.reverse()
#     return value

# def mutate(original_individual:List[Tuple[int,int]], potential_gene:List[Tuple[int,int]])->List[Tuple[int,int]]:
#     individual = [ i for i in original_individual]
#     pos = random.randint(0,len(individual)-1)
#     gene = individual[pos]
#     while gene == individual[pos]:
#         gene = random.sample(potential_gene,1)[0]
#     individual[pos] = gene
#     return individual
def mutate(original_individual:List[Tuple[int,int]], potential_gene:List[Tuple[int,int]])->List[Tuple[int,int]]:
    individual = [ i for i in original_individual]
    pos = random.randint(0,len(individual)-1)
    gene = individual[pos]
    while gene == individual[pos]:
        gene = random.sample(potential_gene,1)[0]
    individual[pos] = gene
    return individual

def crossover(original_individual1:List[Tuple[int,int]],original_individual2:List[Tuple[int,int]]):
    individual1 = [i for i in original_individual1]
    individual2 = [i for i in original_individual2]
    assert len(individual1) == len(individual2),"Individual must have same length!"
    pos = random.randint(0, len(individual1) - 1)
    tem = individual1[pos:]
    individual1[pos:] = individual2[pos:]
    individual2[pos:] = tem
    return individual1,individual2

class Population:
    def __init__(self,board:Board,player:Player,
                 potential_gene:List[Tuple[int,int]],DNA_length = 4,
                 mutate_rate_limit = 0.01,
                 start_number = 2000, number_limit = 3500,
                 survival_rate = 0.1):
        self.board=board
        self.player=player
        self.DNA_base:List[Tuple[int,int]] = potential_gene
        self.DNA_length:int = DNA_length
        self.number_limit:int = number_limit
        self.mutate_rate_limit:float = mutate_rate_limit 
        self.survival_rate:float = survival_rate
        self.best_5:List[Tuple[int,int]] = [(-1,-1) for _ in range(5)] 
        self.currentgeneration:List[List[Tuple[int,int]]] = self.__begin_generation(start_number=start_number)

    def __begin_generation(self,start_number:int)->List[List[Tuple[int,int]]]:
        assert len(self.DNA_base) >= self.DNA_length, "Potential gene is not adequate!"
        generation:List[List[Tuple[int,int]]] = []
        for _ in range(start_number):
            DNA = random.sample(self.DNA_base,min(self.DNA_length,len(self.DNA_base)))
            generation.append(DNA)
        return generation

    def select(self,board:Board,player:Player,opponent:Player):
        print(self.best_5)
        grades = list(map(lambda x: (self.select_function(x,board,player,opponent), x), self.currentgeneration))
        self.currentgeneration = list(map(lambda xy: xy[1],
                                          sorted(grades,key= (lambda x: x[0]),reverse=True)[:int(len(self.currentgeneration)*self.survival_rate)]))

    def findandadd_best(self):
        # this step needs caching
        best_sol = Counter([i[0] for i in self.currentgeneration]).most_common(1)[0]
        del self.best_5[0]
        self.best_5.append(best_sol[0])
        isConvergedYetFlag = best_sol[1] == len(self.currentgeneration) 
        return best_sol[0],isConvergedYetFlag

    def generate_next(self):
        mutate_number = random.randint(0,int(self.mutate_rate_limit* self.number_limit))
        crossover_number = self.number_limit - len(self.currentgeneration) - mutate_number
        valid = 0 
        while valid < crossover_number:
            individual1,individual2 = random.sample(self.currentgeneration,2)
            new_DNA = crossover(individual1,individual2)
            valid += 2
            self.currentgeneration.append(new_DNA[0])
            self.currentgeneration.append(new_DNA[1])
        valid = 0
        while valid < mutate_number:
            selected = random.sample(self.currentgeneration,1)[0]
            new_DNA = mutate(selected,MinmaxStrategy.get_possible_cells(self.board.get_new_board_apply(self.player,selected),[],selected))
            valid += 1
            self.currentgeneration.append(new_DNA)
    def select_function(self,moves:List[Tuple[int,int]],board:Board,player:Player,opponent:Player,n_in_line=5):
        return MinmaxStrategy.evaluate_board(board.get_new_board_apply(player,moves),player,moves,HEURISTIC_SCORES_GENETICS)\
            +MinmaxStrategy.get_cell_importance(board,*moves[0])*10000000
class GeneticStrategy(Strategy):
    def make_move(self,board:Board, player:Player,time_limit=20.0) -> Tuple[int,int]:
        possible_cells=self.get_possible_cells(board)
        population = Population(Board(board.board_size,board.data[:]),player,
                                            possible_cells,DNA_length=4,
                                            mutate_rate_limit=0.01,start_number=200,number_limit=300,
                                            survival_rate=0.1)
        begin_time = time.time()
        gene = 0
        while time.time()-begin_time < time_limit:
            population.select(board,player,getEnemy(player)) 
            gene += 1
            best_sol,stop = population.findandadd_best()
            if stop:
                return best_sol
            if len(set(population.best_5)) == 1:
                return population.best_5[0]
            else:
                population.generate_next() 
        best_5 = Counter(population.best_5).most_common(5)
        for i in range(len(best_5)):
            if best_5[i][0] != (-1,-1):
                return best_5[i][0]
        return possible_cells[0]
    def get_possible_cells(self,board:Board):
        """
            Generates the cells that should be checked further
        """
        x_unfree = list(set([i[0] for i in board.get_filled_cells()]))
        xu = min(x_unfree)
        xb = max(x_unfree) + 1
        y_unfree = list(set([i[1] for i in board.get_filled_cells()]))
        y_unfree.sort()
        # get bounding box around the area where chess pieces has been placed
        # at the same time extend the box in each direction if not out of range.
        yl = min(y_unfree)
        yr = max(y_unfree) + 1
        xu = max(xu-3,0)
        xb =min(xb+3,board.board_height)
        yl = max(yl-3,0)
        yr =min(yr+3,board.board_width)
        print("considering",xu,yl,xb,yr)
        return [
            (i, j) for i in range(xu,xb) for j in range(yl,yr) if board.is_cell_empty(i,j)
        ]