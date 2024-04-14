import random
from pygame import mixer

mixer.init()
max_mines, size_x, size_y, mines, mine, flags, board, field, FlagMode, fbc, fbt, summoned, activated = \
    0, 0, 0, 0, 0, 0, [], [], False, 'light gray', "⛏", [], False


class Difficulty:
    def __init__(self, max_mines, size_y, size_x):
        self.max_mines = max_mines
        self.size_x = size_x
        self.size_y = size_y

    def set(self):
        global max_mines, size_x, size_y, flags
        max_mines = self.max_mines
        flags = self.max_mines
        size_x = self.size_x
        size_y = self.size_y


n = random.randint(8, 10)
Easy = Difficulty(n, n, n)
n = random.choice([13, 16])
if n == 13:
    k = 15
else:
    k = 16
Normal = Difficulty(40, n, k)
Hard = Difficulty(99, 16, 30)
Hell = Difficulty(170, 21, 37)
Super_Hell = Difficulty(180, 21, 37)


class Mine:
    def __init__(self, row, column):
        self.row = row
        self.column = column


def flag_mode():
    global FlagMode, fbc, fbt
    if FlagMode:
        FlagMode = False
        fbc = 'light gray'
        fbt = "⛏"
    else:
        FlagMode = True
        fbc = 'red'
        fbt = "🚩"


def ask_diff():
    print("Choose Difficulty\n[Easy][Normal][Hard]")
    ans = input("=")
    if ans == "Super Hell":
        Super_Hell.set()
    elif ans == "Hell":
        Hell.set()
    elif ans == "Hard":
        Hard.set()
    elif ans == "Normal":
        Normal.set()
    elif ans == "Easy":
        Easy.set()
    else:
        print("Enter a valid difficulty!")
        return ask_diff()


def board_gen():
    global board, summoned
    summoned = []
    board = []
    for y in range(size_y):
        board.append([])
        summoned.append([])
        for x in range(size_x):
            board[y].append(["X"])
            summoned[y].append([])


def left_click(row, column):
    if 1 <= row <= size_y and 1 <= column <= size_x:
        if not activated:
            dig(row, column)
        elif "M" in field[row - 1][column - 1] and "F" not in board[row - 1][column - 1] and not FlagMode:
            board[row - 1][column - 1][0] = field[row - 1][column - 1][0]
            for y in range(size_y):
                for x in range(size_x):
                    if "M" in field[y][x]:
                        board[y][x] = field[y][x]
            mat_print(board)
            print("You lost!")
            exit()
        elif "F" in board[row - 1][column - 1]:
            if FlagMode:
                flag(row, column)
            mixer.music.load('flag place.mp3')
            mixer.music.play()
        elif "1" <= board[row - 1][column - 1][0] <= "8":
            surrounding_flags = 0
            for a in [1, 0, -1]:
                for b in [1, 0, -1]:
                    if 1 <= row + a <= size_y and 1 <= column + b <= size_x:
                        if board[row - 1 + a][column - 1 + b][0] == 'F':
                            surrounding_flags += 1
            if surrounding_flags == int(board[row - 1][column - 1][0]):
                for a in [1, 0, -1]:
                    for b in [1, 0, -1]:
                        dig(row + a, column + b)
        else:
            if FlagMode:
                flag(row, column)
                mixer.music.load('flag place.mp3')
                mixer.music.play()
            else:
                dig(row, column)
        check_win()


def dig(row, column):
    if 1 <= row <= size_y and 1 <= column <= size_x and board[row - 1][column - 1] != ['F']:
        if field[row - 1][column - 1][0] == 'M' and board[row - 1][column - 1][0]:
            mat_print(board)
            print("You lost!")
            exit()
        if '0' not in field[row - 1][column - 1]:
            board[row - 1][column - 1][0] = field[row - 1][column - 1][0]
        elif board[row - 1][column - 1][0] != ' ':
            board[row - 1][column - 1] = [' ']
            if not activated:
                rest_main()
            for a in [1, 0, -1]:
                for b in [1, 0, -1]:
                    dig(row + a, column + b)


def field_gen():
    global field
    field = []
    for y in range(size_y):
        field.append([])
        for x in range(size_x):
            field[y].append(['0'])


def mine_place():
    global mines, mine
    while mines < max_mines:
        mine = Mine(random.randint(0, size_y - 1), random.randint(0, size_x - 1))
        if "0" <= field[mine.row][mine.column][0] <= "7":
            for a in [-2, -1, 0, 1, 2]:
                for b in [-2, -1, 0, 1, 2]:
                    try:
                        if board[mine.row + a][mine.column + b][0] == ' ':
                            return mine_place()
                        else:
                            pass
                    except IndexError:
                        pass
            field[mine.row][mine.column] = ['M']
            for y in [1, 0, -1]:
                for x in [1, 0, -1]:
                    if 0 <= mine.row + y <= size_y - 1 and 0 <= mine.column + x <= size_x - 1:
                        if field[mine.row + y][mine.column + x][0] != 'M':
                            field[mine.row + y][mine.column + x] = [str(
                                int(field[mine.row + y][mine.column + x][0][0]) + 1)]
                        else:
                            pass
                    else:
                        pass
            mines += 1
        else:
            return mine_place()


def flag(row, column):
    global flags
    if board[row - 1][column - 1] == ['X'] and flags > 0:
        board[row - 1][column - 1] = ['F']
        flags -= 1
    elif board[row - 1][column - 1] == ['F']:
        board[row - 1][column - 1] = ['X']
        summoned[row - 1][column - 1] = False
        flags += 1


def mat_print(mat):
    for y in range(size_y):
        for x in range(size_x):
            if x != size_x - 1:
                print(mat[y][x], end="")
            else:
                print(mat[y][x])


def check_win():
    for y in range(size_y):
        for x in range(size_x):
            if "M" in field[y][x] and "X" not in board[y][x] and "F" not in board[y][x]:
                return False
            elif "M" not in field[y][x] and ("X" in board[y][x] or "F" in board[y][x]):
                return False
    print("You Won!")
    exit()


def main():
    ask_diff()
    board_gen()
    field_gen()


def rest_main():
    global activated
    activated = True
    mine_place()
