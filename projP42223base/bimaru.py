# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 116:
# 102500 Alice Mota
# 102618 Ana Margarida Almeida

import sys

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def get_value(self, row: int, col: int) -> str:
        return self.board[row][col]
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        pass

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""

        if row == 0:
            return self.board[row + 1][col]
        elif row == 9:
            return self.board[row - 1][col]
        else:
            up_val = self.board[row - 1][col]
            down_val = self.board[row + 1][col]
            return up_val, down_val
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return self.board[row][col + 1]
        elif col == 9:
            return self.board[row][col - 1]
        else:
            left_val = self.board[row][col - 1]
            right_val = self.board[row][col + 1]
            return left_val, right_val
        # TODO
        pass

    @staticmethod
    def parse_instance():
        # instance.rows
        # instance.cols 
        instance = Board()
        instance.board = [["-" for _ in range(11)] for _ in range(11)]

        from sys import stdin
        values = stdin.readline().lstrip("ROW\t").split('\t')
        instance.rows = [int(value) for value in values]


        values = stdin.readline().lstrip("COLUMN\t").split('\t')
        instance.cols = [int(value) for value in values]

        n_hints = int(stdin.readline().rstrip())

        for i in range(n_hints):
            hint = stdin.readline().lstrip("HINT\t").split('\t')
            #hints = [int(h) for h in hint]
            print(hint[0])
            #print(hint[0])
            print(hint[1])
            print(hint[2].rstrip())
            instance.board[int(hint[0])][int(hint[1])] = hint[2].rstrip()
        
        #print(values)
        
        return instance
   

        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        pass

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    instance = Board.parse_instance()
    print(instance.rows)
    print(instance.cols)
    for j in range(10):
        print(instance.board[j])

    print(instance.get_value(0, 0))
    #print(instance.adjacent_vertical_values(9,5))
    print(instance.adjacent_horizontal_values(0,0))
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
