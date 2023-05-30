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

    def print(self):
        """Mostrar o estado do board"""
        print("===============================================")
        print("Board:")
        for i in range(10):
            for j in range(10):
                print(self.board[i][j]
                      if self.board[i][j] is not None else ".", end=" "
                      )
            print(self.rows[i])
        for i in range(10):
            print(self.cols[i], end=" ")
        print()
        # print(self.cols)
        print("Barcos por colocar = ", self.boats)
        print("Dicas por explorar = ", self.hints)
        print("free_spaces = self.free_spaces")
        print("===============================================")

    def remove_free_space(self, row: int, col: int):
        if self.board[row][col] == None or self.board[row][col] == '.':
            self.free_spaces -= 1

    def place_water(self, row: int, col: int):
        """Coloca àgua na célula dada"""
        if self.get_value(row, col) == None:
            self.remove_free_space(row, col)
            self.board[row][col] = "w"

    def place_top(self, row: int, col: int):
        if self.get_value(row, col) == None:
            self.remove_free_space(row, col)
            self.board[row][col] = "t"
        self.clean_t(row, col)

    def place_middle(self, row: int, col: int):
        if self.get_value(row, col) == None:
            self.remove_free_space(row, col)
            self.board[row][col] = "m"
        self.clean_m(row, col)

    def place_bottom(self, row: int, col: int):
        if self.get_value(row, col) == None:
            self.remove_free_space(row, col)
            self.board[row][col] = "b"
        self.clean_b(row, col)

    def place_right(self, row: int, col: int):
        if self.get_value(row, col) == None:
            self.remove_free_space(row, col)
            self.board[row][col] = "r"
        # self.clean_r(row, col)

    def place_left(self, row: int, col: int):
        if self.get_value(row, col) == None:
            self.remove_free_space(row, col)
            self.board[row][col] = "l"
        self.clean_l(row, col)

    def place_circle(self, row: int, col: int):
        self.remove_free_space(row, col)
        self.board[row][col] = "c"
        self.clean_c(row, col)

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
        self.place_water(row-1, col)
        self.place_water(row+1, col)
        self.place_water(row-1, col-1)
        self.place_water(row, col-1)
        self.place_water(row+1, col-1)
        self.place_water(row+1, col+1)
        self.place_water(row+1, col+2)
        self.place_water(row-1, col+1)
        self.place_water(row-1, col+2)
        # FIXME: não sei se estas duas linhas sao
        # desnecessarias porque depois há repeticao
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

        self.cols[col] -= 1
        if (self.cols[col] == 0):
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

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col == 0:
            left = None
            right = self.board[row][col + 1]

        elif col == 9:
            left = self.board[row][col - 1]
            right = None

        else:
            left = self.board[row][col - 1]
            right = self.board[row][col + 1]

        return left, right

    def is_clear(self, row: int, col: int):
        """Devolve true se for um espaço em branco, false se estiver
        preenchido"""
        return self.board[row][col] == None

    def remove_boat(self, boat_size: int):
        self.boats[0] -= 1
        self.boats[boat_size] -= 1 
    
    def check_if_complete_boats(self, row: int, col: int):
        # When putting a left, checks if it can complete a boat
        type = self.get_value(row, col)
        # Receives an l
        if type == "L":
            if self.get_value(row, col+1) == "R":
                self.remove_boat(2)
                #TODO this is a complete boat
            
            elif col == 8:
                self.place_right(row, col+1)
                self.remove_boat(2)
            
            if row <= 7:
                if self.get_value(row, col+2) == "R":
                    self.place_middle(row, col+1)
                    self.remove_boat(3)
                
            if row <= 6:
                 if self.get_value(row, col+3) == "R":
                    if self.get_value(row, col+1) == None:
                        self.place_middle(row, col+1)
                        self.place_middle(row, col+2)
                        self.remove_boat(4)

        # Receives an r 
        if type == "R":
            if self.get_value(row, col-1) == "L":
                self.remove_boat(2)
                #TODO this is a complete boat
            
            elif col == 1:
                self.place_left(row, col-1)
                self.remove_boat(2)

            if row >= 2:
                if self.get_value(row, col-2) == "L":
                    self.place_middle(row, col-1)
                    self.remove_boat(3)
            
            if row >= 3:
                if self.get_value(row, col-3) == "L":
                    self.place_middle(row, col-1)
                    self.place_middle(row, col-2)
                    self.remove_boat(4)
        
        # Receives a t
        if type == "T":
            if self.get_value(row+1, col) == "B":
                self.remove_boat(2)
            
            elif row == 8:
                self.place_bottom(row+1, col)
                self.remove_boat(2)
            
            if row <= 7:
                if self.get_value(row+2, col) == "B":
                    self.place_middle(row+1, col)
                    self.remove_boat(3)

            if row <= 6:
                if self.get_value(row+3, col) == " B":
                    self.place_middle(row+1, col)
                    self.place_middle(row+2, col)
                    self.remove_boat(4)
        
        # Receives a b
        if type == "B":
            if self.get_value(row-1, col) == "T":
                self.remove_boat(2)
            
            elif row == 1:
                    self.place_top(row-1, col)
                    self.remove_boat(2)
            
            if row >= 2:
                if self.get_value(row-2, col) == "T":
                    self.place_middle(row-1, col)
                    self.remove_boat(3)
            
            if row >= 3:
                if self.get_value(row-3, col) == "T":
                    self.place_middle(row-1, col)
                    self.place_middle(row-2, col)
                    self.remove_boat(4)
        
        # Receives an m
        if type == "M":
            if row == 0:
                self.place_water(row+1, col)
                self.place_water(row+1, col-1)
                self.place_water(row+1, col+1)
            
            if row == 9:
                self.place_water(row-1, col)
                self.place_water(row-1, col-1)
                self.place_water(row-1, col+1)
            
            if col == 0:
                self.place_water(row, col+1)
                self.place_water(row-1, col+1)
                self.place_water(row+1, col+1)

            if col == 9:
                self.place_water(row, col-1)
                self.place_water(row-1, col-1)
                self.place_water(row+1, col-1)
            
            if col <= 7:
                if self.get_value(row, col+2) == "R":
                    self.place_middle(row, col+1)
                    self.place_left(row, col-1)
                    self.remove_boat(4)

            if col >= 2:
                if self.get_value(row, col-2) == "L":
                    self.place_middle(row, col-1)
                    self.place_right(row, col+1)
                    self.remove_boat(4)
            

            if col <= 6:
                if self.get_value(row, col+3) == "R":
                    self.place_left(row, col+2)
                    self.remove_boat(2)
            
            if col >= 3:
                if self.get_value(row, col-3) == "L":
                    self.place_right(row, col-2)
                    self.remove_boat(2)

            if row >= 2:
                if self.get_value(row-2, col) == "T":
                    self.place_middle(row-1, col)
                    self.place_bottom(row+1, col)
                    self.remove_boat(4)

            if row >= 3:
                if self.get_value(row-3, col) == "T":
                    self.place_bottom(row-2, col)
                    self.remove_boat(2)

            if row <= 7:
                if self.get_value(row+2, col) == "B":
                    self.place_top(row-1, col)
                    self.place_middle(row+1, col)
                    self.remove_boat(4)
            
            if row <= 6:
                if self.get_value(row+3, col) == "B":
                    self.place_top(row+2, col)
                    self.remove_boat(2)
                
            
    def createNewBoard(self):
        new_board = Board()
        new_board.rows = self.rows
        new_board.cols = self.cols
        new_board.hints = self.hints.copy()
        new_board.boats = self.boats.copy()
        new_board.board = []
        for i in range(11):
            new_board.board.append(self.board[i].copy())
        new_board.free_spaces = self.free_spaces

        return new_board    

    def set_boat(self, row: int, col: int, size: int, is_horizontal: bool):
        new_board = self.createNewBoard()

        def set_size1():
            new_board.place_circle(row, col)
            self.remove_boat(1)

        def set_size2():
            if is_horizontal:
                if new_board.is_clear(row, col):
                    new_board.place_left(row, col)
                if new_board.is_clear(row, col+1):
                    new_board.place_right(row, col+1)
            else:
                if new_board.is_clear(row, col):
                    new_board.place_top(row, col)
                if new_board.is_clear(row+1, col):
                    new_board.place_bottom(row+1, col)
                    # new_board.clean_b(row,col)
            self.remove_boat(2)

        def set_size3():
            if is_horizontal:
                if new_board.is_clear(row, col):
                    new_board.place_left(row, col)
                if new_board.is_clear(row, col+1):
                    new_board.place_middle(row, col+1)
                if new_board.is_clear(row, col+2):
                    new_board.place_right(row, col)+2
            else:
                if new_board.is_clear(row, col):
                    new_board.place_top(row, col)
                if new_board.is_clear(row+1, col):
                    new_board.place_middle(row+1, col)
                if new_board.is_clear(row+2, col):
                    new_board.place_bottom(row+2, col)
            self.remove_boat(3)

        def set_size4():
            if is_horizontal:
                if new_board.is_clear(row, col):
                    new_board.place_left(row, col)
                if new_board.is_clear(row, col+1):
                    new_board.place_middle(row, col+1)
                if new_board.is_clear(row, col+2):
                    new_board.place_middle(row, col+2)
                if new_board.is_clear(row, col+3):
                    new_board.place_right(row, col+3)
            else:
                if new_board.is_clear(row, col):
                    new_board.place_top(row, col)
                if new_board.is_clear(row+1, col):
                    new_board.place_middle(row+1, col)
                if new_board.is_clear(row+2, col):
                    new_board.place_middle(row+2, col)
                if new_board.is_clear(row+3, col):
                    new_board.place_bottom(row+3, col)
            self.remove_boat(4)

        if size == 1:
            set_size1()
        elif size == 2:
            set_size2()
        elif size == 3:
            set_size3()
        else:
            set_size4()

        return new_board

    # def place_dots(self, h_row: int, h_col: int, h_sym: str):
      #  if h_sym == 'W': self.board[h_row][h_col] = h_sym
     #   else:

    @staticmethod
    def parse_instance():
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
        instance.free_spaces = 100

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
            # print(row)
            # print("col = ", col)
            # print(type)
            instance.board[row][col] = type
            instance.free_spaces -= 1
            instance.clean_cell(row, col, type)
            if (type != "W"):
                # print("hint = ", type)
                instance.reduceValues(row, col)
                instance.check_if_complete_boats(row, col)
                if (type != "C"):
                    instance.hints.append((row, col))
                else:
                    instance.boats[0] -= 1
                    instance.boats[1] -= 1
            # print("free_spaces -> \t")
            # print(instance.free_spaces)

        instance.clean_board()
        # TODO: verificar se já há barcos preenchidos

        # TODO: acho que devemos preencher aquilo que já se pode
        return instance

    def isValidPosition(self, row: int, col: int, type: str):
        # print("isValidPosition")
        # type must be in ["H"(horizontal), "V"(vertical), "C"(center)]
        if self.get_value(row, col) != None:
            # print("not None")
            return False
        if self.rows[row] < 1:
            # print("No space in row")
            return False
        if self.cols[col] < 1:
            # print("No space in col")
            return False

        # not sure se isto é a maneira mais eficiente
        vizinhos_permitidos = ['w', None, "W"]
        valid = True

        # TODO check if é mesmo necessario explorar diagonais

        # verificar diagonais
        valid = self.get_value(row - 1, col - 1) in vizinhos_permitidos
        valid = self.get_value(row - 1, col + 1) in vizinhos_permitidos
        valid = self.get_value(row + 1, col - 1) in vizinhos_permitidos
        valid = self.get_value(row + 1, col + 1) in vizinhos_permitidos
        if not valid:
            return False

        # se não vertical (horizontal or center), verificar cima e baixo
        if type != "V":
            valid = self.get_value(row - 1, col) in vizinhos_permitidos
            valid = self.get_value(row + 1, col) in vizinhos_permitidos
        # se não horizontal (vertical or center), verificar direita e esquerda
        if type != "H":
            valid = self.get_value(row, col-1) in vizinhos_permitidos
            valid = self.get_value(row, col+1) in vizinhos_permitidos
        # print("return valid = ", valid)
        return valid

    def getActionsT(self, row, col):
        validActions = []
        for size in range(2, 5):
            print(size)
            if (self.cols[col] < size - 1 or self.rows[row+size-1] < 1 or not self.isValidPosition(row+size-1, col, "V")):
                break
            if self.boats[size] < 1:
                # já foram colocados todos os barcos deste tamanho
                continue
            validActions.append((row, col, size, False))
        # FIXME: ver se apanha outra dica
        print("getActionsT = ", validActions)
        return validActions

    def getActionsB(self, row, col):
        validActions = []
        for size in range(2, 5):
            print(size)
            if (self.cols[col] < size - 1 or self.rows[row-size+1] < 1 or not self.isValidPosition(row-size+1, col, "V")):
                break
            if self.boats[size] < 1:
                # já foram colocados todos os barcos deste tamanho
                continue
            validActions.append((row-size+1, col, size, False))
        # FIXME: ver se apanha outra dica
        print("getActionsB = ", validActions)
        return validActions

    def getActionsR(self, row, col):
        validActions = []
        for size in range(2, 5):
            print(size)
            if (self.cols[col-size+1] < 1 or self.rows[row] < size - 1 or not self.isValidPosition(row, col-size+1, "H")):
                break
            if self.boats[size] < 1:
                # já foram colocados todos os barcos deste tamanho
                continue
            validActions.append((row, col-size+1, size, True))
        # FIXME: ver se apanha outra dica
        print("getActionsR = ", validActions)
        return validActions

    def getActionsM(self, row, col):
        validActions = []
        if self.isValidPosition(row-1, col, "V") and self.isValidPosition(row+1, col, "V") and self.cols[col] >= 2:
            # check posicoes verticais
            validActions.append((row-1, col, 3, False))
            if self.cols[col] >= 3:
                if self.isValidPosition(row-2, col, "V"):
                    validActions.append((row-2, col, 4, False))
                if self.isValidPosition(row+2, col, "V"):
                    validActions.append((row-1, col, 4, False))

        if self.isValidPosition(row, col-1, "H") and self.isValidPosition(row, col+1, "H") and self.rows[row] >= 2:
            # check posicoes horizontais
            validActions.append((row, col-1, 3, True))
            if self.rows[row] >= 3:
                if (self.isValidPosition(row, col-2, "H")):
                    validActions.append((row, col-2, 4, True))
                if (self.isValidPosition(row, col+2, "H")):
                    validActions.append((row, col-1, 4, True))
        print("getActionsM = ", validActions)
        return validActions

    def getActionsL(self, row, col):
        validActions = []
        for size in range(2, 5):
            print(size)
            if (self.cols[col+size-1] < 1 or self.rows[row] < size - 1 or not self.isValidPosition(row, col+size-1, "H")):
                break
            if self.boats[size] < 1:
                # já foram colocados todos os barcos deste tamanho
                continue
            validActions.append((row, col, size, True))
        # FIXME: ver se apanha outra dica
        print("getActionsL = ", validActions)
        return validActions

    def isValid(self, row, col, isHorizontal, size):
        # print("isValid4")
        # print(row, col, isHorizontal)
        if isHorizontal and self.rows[row] < size:
            # print("isHorizontal")
            return False
        if not isHorizontal and self.cols[col] < size:
            # print("self.cols[col] < 4")
            return False

        for i in range(1, size):
            if isHorizontal and self.get_value(row, col+i) != None:
                # print("isHorizontal 2")
                return False
            if not isHorizontal and self.get_value(row+i, col) != None:
                # print("self.get_value(row, col+i)")
                return False
        # print("saiu true")
        return True

    def getAll(self, size):
        validActions = []
        for row in range(10):
            for col in range(10):
                if self.get_value(row, col) == None:
                    if col <= 10-size and self.isValid(row, col, True, size):
                        validActions.append((row, col, size, True))
                    if row <= 10-size and self.isValid(row, col, False, size):
                        validActions.append((row, col, size, False))
        print("validActions = ", validActions)
        return validActions

    # def getVerticalActions(self, row, col, type):
    #     print("vertical actions", type)

    # def getHorizontalActions(self, row, col, type):
    #     pass
    # TODO: outros metodos da classe

    def get_nfrees_col(self, col: int) -> int:
        n_frees_col = 0
        for i in range(10):
            if self.board[i][col] == (None or '.'):
                n_frees_col += 1
        return n_frees_col

    def get_nfrees_row(self, row: int) -> int:
        n_frees_row = 0
        for i in range(10):
            if self.board[row][i] == (None or '.'):
                n_frees_row += 1
        return n_frees_row

    def isInvalidBoard(self):
        """ for i in range (10):
        for i in range(10):
            if (self.rows[i] < 0) or (self.cols[i] < 0):
                return True -> check if is not necessary"""

        if self.free_spaces < self.boats[0]:
            return True

        if self.free_spaces < (self.boats[1] + self.boats[2]*2 + self.boats[3]*3 + self.boats[4]*4):
            return True

        for i in range(10):
            if (self.board.rows[i] > self.get_nfrees_row(i)) or (self.board.cols[i] > self.get_nfrees_col(i)):
                return True

        # TODO complete


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        print("ENTREI ACTIONS")
        # TODO -> se houver hints por explorar, vemos as hints
        # return [(row,col,size,ishorizontal:true)]
        board = state.board
        # id = state.id
        # print(state)
        # print(board)
        # print(id)
        # state.print()
        # print("AAAAAAAAAAAAAAA")
        # board.print()

        # ver se ainda há dicas para explorar
        if len(board.hints) > 0:
            # print("explorar dicas")
            row = board.hints[-1][0]
            col = board.hints[-1][1]
            # remover a dica das dicas a serem exploradas
            board.hints.pop()
            type = board.get_value(row, col).lower()
            if type == "t":
                return board.getActionsT(row, col)
            if type == "b":
                return board.getActionsB(row, col)
            if type == "l":
                return board.getActionsL(row, col)
            if type == "r":
                return board.getActionsR(row, col)
            if type == "m":
                return board.getActionsM(row, col)
        else:
            if board.boats[0] > 0:
                for i in range(4, 0, -1):
                    if board.boats[i] > 0:
                        return board.getAll(i)
        return []

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        print("ENTREI RESULT")
        (row, col, size, is_horizontal) = action
        print(row, col, size, is_horizontal)
        state.board.print()
        return BimaruState(state.board.set_boat(row, col, size, is_horizontal))
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO -> ver se todos os barcos estão a 0
        print("entrei goal_test")
        print(state)
        return False
        # return state.board.board.boats[0] == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance()
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    initial_state = BimaruState(board)
    # print(instance.rows)
    # print(instance.cols)
    # print("\n")
    # for j in range(10):
    #     print(instance.rows[j], " ", instance.board[j])

    # print(instance.get_value(0, 0))
    # print(instance.adjacent_vertical_values(9,5))
    # print(instance.adjacent_horizontal_values(0, 0))
    # print(instance.hints)

    # print(instance.adjacent_vertical_values(9, 5))

    # board.print()
    # print(problem.goal_test(initial_state))
    # actions = problem.actions(initial_state)
    # for action in actions:
    #     print(action)
    # print(actions)
    # print("new")

    # new_state = problem.result(initial_state, (0, 6, 3, False))
    # new_state.board.print()

    goal_node = depth_first_tree_search(problem)
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.print(), sep="")

    # print(board.board)
    # new_board.board[5][5] = "E"

    # board.print()
    # new_board.print()

# Ler o ficheiro do standard input,
# Usar uma técnica de procura para resolver a instância,
# Retirar a solução a partir do nó resultante,
# Imprimir para o standard output no formato indicado.
pass
