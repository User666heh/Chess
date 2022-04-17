from tkinter import * #вот тут, конечно, согрешил


WHITE = 1
BLACK = 2


def start():
    global board
    board = Board()
    canvas.delete("all")

    for i in range(8):
        for j in range(8):
            if board.field[i][j] is not None:
                pic = PhotoImage(file=str(type(board.field[i][j])).split('.')[1][:-2]+'.png')
                canvas.create_image(i*60, j*60, image=pic)


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(0, 0, WHITE), Knight(0, 1, WHITE), Bishop(0, 2, WHITE), Queen(0, 3, WHITE),
            King(0, 4, WHITE), Bishop(0, 5, WHITE), Knight(0, 6, WHITE), Rook(0, 7,WHITE)
        ]
        self.field[1] = [
            Pawn(1, 0, WHITE), Pawn(1, 1, WHITE), Pawn(1, 2, WHITE), Pawn(1, 3, WHITE),
            Pawn(1, 4, WHITE), Pawn(1, 5, WHITE), Pawn(1, 6, WHITE), Pawn(1, 7, WHITE)
        ]
        self.field[6] = [
            Pawn(6, 0, BLACK), Pawn(6, 1, BLACK), Pawn(6, 2, BLACK), Pawn(6, 3, BLACK),
            Pawn(6, 4, BLACK), Pawn(6, 5, BLACK), Pawn(6, 6, BLACK), Pawn(6, 7, BLACK)
        ]
        self.field[7] = [
            Rook(7, 0, BLACK), Knight(7, 1, BLACK), Bishop(7, 2, BLACK), Queen(7, 3, BLACK),
            King(7, 4, BLACK), Bishop(7, 5, BLACK), Knight(7, 6, BLACK), Rook(7, 7, BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if not piece.can_move(row1, col1):
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True

    def is_under_attack(self, row, col, color):
        piece = self.field
        for i in range(len(piece)):
            for j in range(len(piece)):
                if piece[i][j] is not None:
                    if piece[i][j].get_color() == color and piece[i][j].can_move(row, col):
                        return True
        return False


class Queen:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row, col):
        if (0 <= row < 8) and (0 <= col < 8) and ((abs(self.row - row) == abs(self.col - col)) or self.col == col or self.row == row) and board[row, col] is None:
            if self.row == row or self.col == col:
                if self.row == row:
                    need = [self.col, col, 1]
                    if self.col > col:
                        need[0], need[1], need[2] = need[1], need[0], -1
                else:
                    need = [self.row, row, 1]
                    if self.row > row:
                        need[0], need[1], need[2] = need[1], need[0], -1
                for i in range(need[0], need[1], need[2]):
                    if self.col == col and board[row, i] is not None:
                        return False
                    if self.row == row and board[i, col] is not None:
                        return False
                return True
            elif abs(self.row - row) == abs(self.col - col):
                coord = [self.row, self.col]
                while coord != [row, col]:
                    coord[0] += (self.row - row) / abs(self.row - row)
                    coord[1] += (self.col - col) / abs(self.col - col)
                    if board[coord[0], coord[1]] is not None:
                        return False
                return True

        return False

    def set_position(self, row, col):
        if row >= 0 and col >= 0:
            self.row = row
            self.col = col

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'


class Bishop:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row, col):
        if correct_coords(row, col) and (abs(self.row - row) == abs(self.col - col)):
            coord = [self.row, self.col]
            while coord != [row, col]:
                coord[0] += (self.row - row)/abs(self.row - row)
                coord[1] += (self.col - col)/abs(self.col - col)
                if board[coord[0], coord[1]] is not None:
                    return False
            return True
        return False
    def set_position(self, row, col):
        if row >= 0 and col >= 0:
            self.row = row
            self.col = col

    def get_color(self):
        return self.color

    def char(self):
        return 'B'


class Knight:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row, col):
        if correct_coords(row, col) and (((row - 2 == self.row or row + 2 == self.row) and (col - 1 == self.col or col + 1 == self.col)) or ((row - 1 == self.row or row + 1 == self.row) and (col - 2 == self.col or col + 2 == self.col))) and board[row, col] is None:
            return True
        return False

    def set_position(self, row, col):
        if row >= 0 and col >= 0:
            self.row = row
            self.col = col

    def get_color(self):
        return self.color

    def char(self):
        return 'N'


class Pawn:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'P'


    def get_color(self):
        return self.color

    def can_move(self, row, col):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if self.col != col:
            return False
        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if self.row + direction == row and board[row, col] is None:
            return True

        # ход на 2 клетки из начального положения
        if self.row == start_row and self.row + 2 * direction == row and board[row, col] is None:
            return True

        return False


class Rook:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'R'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if self.row == row or self.col == col and board[row, col] is None:
            if self.row == row:
                need = [self.col, col, 1]
                if self.col > col:
                    need[0], need[1], need[2] = need[1], need[0], -1
            else:
                need = [self.row, row, 1]
                if self.row > row:
                    need[0], need[1], need[2] = need[1], need[0], -1
            for i in range(need[0], need[1], need[2]):
                if self.col == col and board[row, i] is not None:
                    return False
                if self.row == row and board[i, col] is not None:
                    return False
            return True
        return False

    def can_attack(self, row, col):
        return self.can_move(row, col)


class King:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
master = Tk()
label = Label(master, text="Шахматы")
label.pack()
canvas = Canvas(master, bg='black', height=600, width=600)
canvas.pack()
start()
master.mainloop()