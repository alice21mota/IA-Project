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

    def place_water(self, row: int, col: int):
        """Coloca àgua na célula dada"""
        self.board[row][col] = "w"
    
    def place_top(self, row: int, col: int):
        self.board[row][col] = "t"
    
    def place_middle(self, row: int, col: int):
        self.board[row][col] = "m"
    
    def place_bottom(self, row: int, col: int):
        self.board[row][col] = "b"
    
    def place_right(self, row: int, col: int):
        self.board[row][col] = "r"
    
    def place_left(self, row: int, col: int):
        self.board[row][col] = "l"
    
    def place_circle(self, row: int, col: int):
        self.board[row][col] = "c"
    
    
    def clean_t(self, row: int, col: int):
        self.place_water(row-1, col-1)
        self.place_water(row-1, col)
        self.place_water(row-1, col+1)
        self.place_water(row, col-1)
        self.place_water(row, col+1)
        # FIXME: não sei se estas duas linhas sao
        self.place_water(row+1, col-1)
        # desnecessarias porque depois há repeticao
        self.place_water(row+1, col+1)
        self.place_water(row+2, col-1)
        self.place_water(row+2, col+1)

    def clean_c(self, row: int, col: int):
        self.place_water(row-1, col-1)
        self.place_water(row-1, col)
        self.place_water(row-1, col+1)
        self.place_water(row, col-1)
        self.place_water(row, col+1)
        self.place_water(row+1, col-1)
        self.place_water(row+1, col)
        self.place_water(row+1, col+1)

    def clean_m(self, row: int, col: int):
        self.place_water(row-1, col-1)
        self.place_water(row-1, col+1)
        self.place_water(row+1, col-1)
        self.place_water(row+1, col+1)
        # nao sei se esta funcao faz sentido sequer
        # diria que ela não existe e mantem se as "repeticoes"
        # todo
        pass

    def clean_b(self, row: int, col: int):
        self.place_water(row, col-1)
        self.place_water(row, col+1)
        self.place_water(row+1, col-1)
        self.place_water(row+1, col)
        self.place_water(row+1, col+1)
        # FIXME: não sei se estas duas linhas sao
        self.place_water(row-1, col-1)
        # desnecessarias porque depois há repeticao
        self.place_water(row-1, col+1)
        self.place_water(row-2, col-1)
        self.place_water(row-2, col+1)

    def clean_l(self, row: int, col: int):
        self.place_water(row-1, col-1)
        self.place_water(row-1, col)
        self.place_water(row-1, col+1)
        self.place_water(row, col-1)
        self.place_water(row, col+1)
        # FIXME: não sei se estas duas linhas sao
        self.place_water(row+1, col-1)
        # desnecessarias porque depois há repeticao
        self.place_water(row+1, col+1)
        self.place_water(row-1, col+2)
        self.place_water(row+1, col+2)
        pass

    def clean_r(self, row: int, col: int):
        self.place_water(row-1, col-2)
        self.place_water(row-1, col-1)
        self.place_water(row-1, col)
        self.place_water(row-1, col+1)
        self.place_water(row, col+1)
        self.place_water(row+1, col-2)
        self.place_water(row+1, col-1)
        self.place_water(row+1, col)
        self.place_water(row+1, col+1)

    def clean_cell(self, row: int, col: int, type: str):
        # FIXME não sei se é mais eficiente passar o tipo ou calcular o tipo aqui
        """Coloca àgua à volta da célula recebida"""
        type = type.lower()
        print("type = ", type)
        if (type == "t"):
            self.clean_t(row, col)
        elif (type == "b"):
            self.clean_b(row, col)
        elif (type == "c"):
            self.clean_c(row, col)
        elif (type == "l"):
            self.clean_l(row, col)
        elif (type == "r"):
            self.clean_r(row, col)
        elif (type == "m"):
            self.clean_m(row, col)

    def clean_row(self, row: int):
        """Preenche os espaços vazios da linha com àgua"""
        for col in range(10):
            if (self.board[row][col] == None):
                self.place_water(row, col)

    def clean_col(self, col: int):
        """Preenche os espaços vazios da linha com àgua"""
        for row in range(10):
            if (self.board[row][col] == None):
                self.place_water(row, col)

    def clean_rows(self):
        """Coloca àgua em todas as linhas que já têm o número total de barcos"""
        for row in range(10):
            if self.rows[row] == 0:
                self.clean_row(row)

    def clean_cols(self):
        """Coloca àgua em todas as colunas que já têm o número total de barcos"""
        for col in range(10):
            if self.cols[col] == 0:
                self.clean_col(col)

    def clean_board(self):
        self.clean_cols()
        self.clean_rows()

    def reduceValues(self, row: int, col: int):
        self.rows[row] -= 1
        if (self.rows[row] == 0):
            self.clean_row(row)
        self.cols[row] -= 1
        if (self.cols[row] == 0):
            self.clean_col(col)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""

        if row == 0:
            up = None
            down = self.board[row + 1][col]

        elif row == 9:
            up = self.board[row - 1][col]
            down = None

        else:
            up = self.board[row - 1][col]
            down = self.board[row + 1][col]

        return up, down
<<<<<<< Updated upstream
=======
        # TODO
        pass
>>>>>>> Stashed changes

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col == 0:
            left = None
            right = self.board[row][col + 1]
<<<<<<< Updated upstream

        elif col == 9:
            left = self.board[row][col - 1]
            right = None

=======
        
        elif col == 0:
            left = self.board[row][col - 1]
            right = None
        
>>>>>>> Stashed changes
        else:
            left = self.board[row][col - 1]
            right = self.board[row][col + 1]

        return left, right
<<<<<<< Updated upstream
    
    def is_clear(self, row: int, col: int):
        """Devolve true se for um espaço em branco, false se estiver
        preenchido"""
        return self.board[row][col] == None

    
    def set_boat(self, row: int, col: int, size: int, is_horizontal: bool):
        new_board = Board()
        new_board = self
        
        def set_size1():
            new_board.place_circle(row, col)

        def set_size2():
            if is_horizontal:
                if new_board.is_clear(row, col):
                    new_board.place_left(row, col)
                if new_board.is_clear(row, col+1):
                    new_board.place_right(row, col)
            else:
                if new_board.is_clear(row, col):
                    new_board.place_top(row, col)
                if new_board.is_clear(row+1, col):
                    new_board.place_bottom(row, col)
        
        def set_size3():
            if is_horizontal:
                if new_board.is_clear(row, col):
                    new_board.place_left(row, col)
                if new_board.is_clear(row, col+1):
                    new_board.place_middle(row, col)
                if new_board.is_clear(row, col+2):
                    new_board.place_left(row, col)
            else:
                if new_board.is_clear(row, col):
                    new_board.place_top(row, col)
                if new_board.is_clear(row+1, col):
                    new_board.place_middle(row, col)
                if new_board.is_clear(row+2, col):
                    new_board.place_bottom(row, col)
        
        def set_size4():
            if is_horizontal:
                if new_board.is_clear(row, col):
                    new_board.place_left(row, col)
                if new_board.is_clear(row, col+1):
                    new_board.place_middle(row, col)
                if new_board.is_clear(row, col+2):
                    new_board.place_middle(row, col)
                if new_board.is_clear(row, col+3):
                    new_board.place_left(row, col)
            else:
                if new_board.is_clear(row, col):
                    new_board.place_top(row, col)
                if new_board.is_clear(row+1, col):
                    new_board.place_middle(row, col)
                if new_board.is_clear(row+2, col):
                    new_board.place_middle(row, col)
                if new_board.is_clear(row+3, col):
                    new_board.place_bottom(row, col)
        
        if size == 1: set_size1()
        elif size == 2: set_size2()
        elif size == 3: set_size3()
        else: set_size4()

        return new_board
    
=======
        # TODO
        pass
>>>>>>> Stashed changes

    #def place_dots(self, h_row: int, h_col: int, h_sym: str):
      #  if h_sym == 'W': self.board[h_row][h_col] = h_sym
     #   else:
            



    @staticmethod
    def parse_instance():
<<<<<<< Updated upstream
=======
        # instance.rows
        # instance.cols 
        instance = Board()
        instance.board = [[None for _ in range(11)] for _ in range(11)]

        from sys import stdin
        values = stdin.readline().lstrip("ROW\t").split('\t')
        instance.rows = [int(value) for value in values]


        values = stdin.readline().lstrip("COLUMN\t").split('\t')
        instance.cols = [int(value) for value in values]

        n_hints = int(stdin.readline().rstrip())

        for i in range(n_hints):
            hint = stdin.readline().lstrip("HINT\t").split('\t')
            instance.board[int(hint[0])][int(hint[1])] = hint[2].rstrip()
        
        return instance
   

>>>>>>> Stashed changes
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # instance.rows
        # instance.cols
        instance = Board()
        # FIXME: pôr àgua nas linhas a mais
        instance.board = [[None for _ in range(11)] for _ in range(11)]
        instance.boats = [10, 4, 3, 2, 1]

        for i in range(11):
            instance.board[i][10] = 'w'
            instance.board[10][i] = 'w'

        from sys import stdin
        values = stdin.readline().lstrip("ROW\t").split('\t')
        instance.rows = [int(value) for value in values]

        values = stdin.readline().lstrip("COLUMN\t").split('\t')
        instance.cols = [int(value) for value in values]

        n_hints = int(stdin.readline().rstrip())

        instance.hints = []
        for i in range(n_hints):
            hint = stdin.readline().lstrip("HINT\t").split('\t')
            # hints = [int(h) for h in hint]
            row = int(hint[0])
            col = int(hint[1])
            type = hint[2].rstrip()
            print(row)
            print(col)
            print(type)
            instance.board[row][col] = type
            instance.clean_cell(row, col, type)
            if (type != "W"):
                print("hint = ", type)
                instance.reduceValues(row, col)
            instance.hints.append((row, col))

        instance.clean_board()

        # print(values)

        return instance

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO -> se houver hints por explorar, vemos as hints
        # return [(row,col,size,ishorizontal:true)]
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row,col,size,is_horizontal) = action
        return BimaruState(state.board.set_boat(row,col,size,is_horizontal))
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO -> ver se todos os barcos estão a 0
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    instance = Board.parse_instance()
    #print(instance.rows)
    #print(instance.cols)
    print("\n")
    for j in range(10):

        print(instance.rows[j], " ", instance.board[j])

    print(instance.get_value(0, 0))
<<<<<<< Updated upstream
    # print(instance.adjacent_vertical_values(9,5))
    print(instance.adjacent_horizontal_values(0, 0))
    print(instance.hints)
=======
    print(instance.adjacent_vertical_values(9,5))
>>>>>>> Stashed changes
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
